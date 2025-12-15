from __future__ import annotations

from typing import List, Dict

from .request import Request
from .driver import Driver
from .dispatch_policies import DispatchPolicy
from .request_generator import RequestGenerator
from .mutation_rules import MutationRule
from .offer import Offer


class DeliverySimulation:
    """
    Main simulation engine.

    Controls time, drivers, requests, and statistics.
    """

    def __init__(
        self,
        drivers: List[Driver],
        dispatch_policy: DispatchPolicy,
        request_generator: RequestGenerator,
        mutation_rule: MutationRule,
        timeout: int,
        *,
        base_fee: float = 10.0,
        distance_fee: float = 1.0,
    ) -> None:
        """
        Create a simulation instance.
        """
        self.time = 0
        self.drivers = drivers
        self.requests: List[Request] = []

        self.dispatch_policy = dispatch_policy
        self.request_generator = request_generator
        self.mutation_rule = mutation_rule
        self.timeout = timeout

        self.served_count = 0
        self.expired_count = 0
        self.wait_times: List[int] = []

        self.base_fee = base_fee
        self.distance_fee = distance_fee

        for d in self.drivers:
            if not hasattr(d, "total_earnings"):
                d.total_earnings = 0.0

    def tick(self) -> None:
        """
        Advance the simulation by one time step.
        """
        self.time += 1

        new_requests = self.request_generator.maybe_generate(self.time)
        self.requests.extend(new_requests)

        self._expire_old_requests()

        offers = self.dispatch_policy.assign(
            self.drivers,
            self._active_requests(),
            self.time,
        )

        accepted = self._filter_acceptances(offers)
        assignments = self._resolve_conflicts(accepted)
        self._apply_assignments(assignments)

        self._move_drivers_and_handle_events()
        self._apply_mutations()

    def get_snapshot(self) -> Dict:
        """
        Return current state in GUI-friendly format.
        """
        return {
            "time": self.time,
            "served": self.served_count,
            "expired": self.expired_count,
            "avg_wait": self._avg_wait(),
            "drivers": [
                {
                    "id": d.did,
                    "x": d.position.x,
                    "y": d.position.y,
                    "status": d.status,
                    "earnings": d.total_earnings,
                }
                for d in self.drivers
            ],
            "pickups": [
                (r.pickup.x, r.pickup.y)
                for r in self.requests
                if r.status in ("WAITING", "ASSIGNED")
            ],
            "dropoffs": [
                (r.dropoff.x, r.dropoff.y)
                for r in self.requests
                if r.status == "PICKED"
            ],
        }

    def _active_requests(self) -> List[Request]:
        """
        Return requests that are not finished.

        --- DOCTEST ---
        >>> class R:
        ...     def __init__(self, active): self._a = active
        ...     def is_active(self): return self._a
        >>> sim = DeliverySimulation.__new__(DeliverySimulation)
        >>> sim.requests = [R(True), R(False), R(True)]
        >>> len(sim._active_requests())
        2
        """
        return [r for r in self.requests if r.is_active()]

    def _expire_old_requests(self) -> None:
        """
        Expire requests that waited longer than timeout.

        --- DOCTEST ---
        >>> class R:
        ...     def __init__(self, t, status="WAITING"):
        ...         self.creation_time = t
        ...         self.status = status
        ...     def is_active(self): return True
        ...     def mark_expired(self, t): self.status = "EXPIRED"
        >>> sim = DeliverySimulation.__new__(DeliverySimulation)
        >>> sim.time = 10
        >>> sim.timeout = 3
        >>> sim.expired_count = 0
        >>> r = R(0)
        >>> sim.requests = [r]
        >>> sim._expire_old_requests()
        >>> r.status
        'EXPIRED'
        """
        for r in self._active_requests():
            if self.time - r.creation_time > self.timeout and r.status != "PICKED":
                r.mark_expired(self.time)
                self.expired_count += 1

    def _filter_acceptances(self, offers: List[Offer]) -> List[Offer]:
        """
        Keep only offers accepted by drivers.

        --- DOCTEST ---
        >>> class B:
        ...     def decide(self, d, o, t): return True
        >>> class D:
        ...     def __init__(self): self.behaviour = B()
        >>> class O:
        ...     def __init__(self): self.driver = D()
        >>> sim = DeliverySimulation.__new__(DeliverySimulation)
        >>> sim.time = 0
        >>> len(sim._filter_acceptances([O(), O()]))
        2
        """
        accepted = []
        for offer in offers:
            if offer.driver.behaviour.decide(offer.driver, offer, self.time):
                accepted.append(offer)
        return accepted

    def _resolve_conflicts(self, accepted: List[Offer]) -> List[Offer]:
        """
        Ensure each request is used once.

        --- DOCTEST ---
        >>> class R:
        ...     def __init__(self, i): self.rid = i
        >>> class O:
        ...     def __init__(self, r): self.request = r
        >>> sim = DeliverySimulation.__new__(DeliverySimulation)
        >>> r = R(1)
        >>> len(sim._resolve_conflicts([O(r), O(r)]))
        1
        """
        used = set()
        result = []

        for offer in accepted:
            rid = offer.request.rid
            if rid in used:
                continue
            used.add(rid)
            result.append(offer)

        return result

    def _apply_assignments(self, assignments: List[Offer]) -> None:
        """
        Assign drivers to requests.
        """
        for offer in assignments:
            driver = offer.driver
            req = offer.request

            if driver.status != "IDLE" or req.status != "WAITING":
                continue

            driver.assign_request(req, self.time)
            req.mark_assigned(driver.did)

    def _move_drivers_and_handle_events(self) -> None:
        """
        Move drivers and handle pickup/dropoff.
        """
        for d in self.drivers:
            req = d.current_request
            if req is None:
                continue

            before = req.status
            d.step(dt=1.0)

            if before in ("WAITING", "ASSIGNED") and d.at_target_location():
                d.complete_pickup(self.time)
                req.mark_picked(self.time)

            elif before == "PICKED" and d.at_target_location():
                d.complete_dropoff(self.time)
                req.mark_delivered(self.time)

                self.served_count += 1
                self.wait_times.append(self.time - req.creation_time)

                d.total_earnings += self._compute_earnings(req)
                d.current_request = None

    def _apply_mutations(self) -> None:
        """
        Possibly change driver behaviour.
        """
        for d in self.drivers:
            self.mutation_rule.maybe_mutate(d, self.time)

    def _compute_earnings(self, req: Request) -> float:
        """
        Compute reward for a delivered request.

        --- DOCTEST ---
        >>> class P:
        ...     def __init__(self, x, y): self.x, self.y = x, y
        ...     def distance_to(self, o):
        ...         return ((self.x-o.x)**2 + (self.y-o.y)**2) ** 0.5
        >>> class R:
        ...     def __init__(self):
        ...         self.pickup = P(0, 0)
        ...         self.dropoff = P(3, 4)
        >>> sim = DeliverySimulation.__new__(DeliverySimulation)
        >>> sim.base_fee = 10.0
        >>> sim.distance_fee = 2.0
        >>> sim._compute_earnings(R())
        20.0
        """
        distance = req.pickup.distance_to(req.dropoff)
        return self.base_fee + self.distance_fee * distance

    def _avg_wait(self) -> float:
        """
        Return average waiting time.

        --- DOCTEST ---
        >>> sim = DeliverySimulation.__new__(DeliverySimulation)
        >>> sim.wait_times = []
        >>> sim._avg_wait()
        0.0
        >>> sim.wait_times = [1, 2, 3]
        >>> sim._avg_wait()
        2.0
        """
        if not self.wait_times:
            return 0.0
        return sum(self.wait_times) / len(self.wait_times)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
