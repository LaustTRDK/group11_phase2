from __future__ import annotations
from typing import List, Dict, Tuple

from .request import Request
from .driver import Driver
from .dispatch_policies import DispatchPolicy
from .request_generator import RequestGenerator
from .mutation_rules import MutationRule


class DeliverySimulation:
    """
    Orchestrates the entire delivery simulation for Phase 2.

    The class follows the simulation pipeline described in the assignment:
      1. Request generation
      2. Request expiration
      3. Dispatch (offer proposals)
      4. Driver accept / reject
      5. Conflict resolution
      6. Assignment
      7. Movement, pickup, and dropoff
      8. Driver mutation

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
    ):
        """
        Initialize the simulation engine.

        Parameters
        ----------
        drivers : list[Driver]
            All drivers participating in the simulation.
        dispatch_policy : DispatchPolicy
            Policy used to propose driver-request matches.
        request_generator : RequestGenerator
            Object responsible for generating new requests.
        mutation_rule : MutationRule
            Rule that may change driver behaviour over time.
        timeout : int
            Maximum waiting time before a request expires.
        base_fee : float, optional
            Fixed earnings per completed request.
        distance_fee : float, optional
            Earnings per unit distance from pickup to dropoff.
        """
        self.time: int = 0
        self.drivers = drivers
        self.requests: List[Request] = []

        self.dispatch_policy = dispatch_policy
        self.request_generator = request_generator
        self.mutation_rule = mutation_rule
        self.timeout = timeout

        # Statistics
        self.served_count = 0
        self.expired_count = 0
        self.wait_times: List[int] = []

        # Earnings model
        self.base_fee = base_fee
        self.distance_fee = distance_fee

        # Ensure all drivers have an earnings attribute
        for d in self.drivers:
            if not hasattr(d, "earnings"):
                d.earnings = 0.0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def tick(self) -> None:
        """
        Advance the simulation by one discrete time step.

        This method implements the full simulation pipeline.
        """
        self.time += 1

        # 1. Generate new requests
        new_requests = self.request_generator.maybe_generate(self.time)
        self.requests.extend(new_requests)

        # 2. Expire old requests
        self._expire_old_requests()

        # 3. Propose assignments
        offers = self.dispatch_policy.assign(
            self.drivers,
            self._active_requests(),
            self.time,
        )

        # 4. Ask drivers to accept or reject
        accepted = self._filter_acceptances(offers)

        # 5. Resolve conflicts
        assignments = self._resolve_conflicts(accepted)

        # 6. Apply assignments
        self._apply_assignments(assignments)

        # 7. Move drivers and handle events
        self._move_drivers_and_handle_events()

        # 8. Apply mutation rules
        self._apply_mutations()

    def get_snapshot(self) -> Dict:
        """
        Return a snapshot of the current simulation state.

        The returned dictionary is intended for use by the GUI adapter.
        """
        return {
            "time": self.time,
            "served": self.served_count,
            "expired": self.expired_count,
            "avg_wait": self._avg_wait(),
            "drivers": [
                {
                    "id": d.id,
                    "x": d.position.x,
                    "y": d.position.y,
                    "status": d.status,
                    "earnings": d.earnings,
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

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _active_requests(self) -> List[Request]:
        """
        Return all requests that are still active.

        A request is considered active if it is not delivered or expired.
        """
        return [r for r in self.requests if r.is_active()]

    def _expire_old_requests(self) -> None:
        """
        Mark requests as expired if they waited longer than the timeout.
        """
        for r in self._active_requests():
            if self.time - r.creation_time > self.timeout and r.status != "PICKED":
                r.mark_expired(self.time)
                self.expired_count += 1

    def _filter_acceptances(
        self,
        offers: List[Tuple[Driver, Request]],
    ) -> List[Tuple[Driver, Request]]:
        """
        Ask each driver whether they accept the offered request.
        """
        accepted = []
        for driver, req in offers:
            if driver.behaviour.decide(driver, req, self.time):
                accepted.append((driver, req))
        return accepted

    def _resolve_conflicts(
        self,
        accepted: List[Tuple[Driver, Request]],
    ) -> List[Tuple[Driver, Request]]:
        """
        Resolve conflicts where multiple drivers accepted the same request.

        The rule is simple: the first accepting driver wins.

        Doctest
        -------
        >>> class D: pass
        >>> class R:
        ...     def __init__(self, id): self.id = id
        >>> d1, d2 = D(), D()
        >>> r = R(1)
        >>> sim = DeliverySimulation([], None, None, None, 10)
        >>> result = sim._resolve_conflicts([(d1, r), (d2, r)])
        >>> len(result)
        1
        """
        assigned_requests = set()
        final = []

        for driver, req in accepted:
            if req.id in assigned_requests:
                continue
            assigned_requests.add(req.id)
            final.append((driver, req))

        return final

    def _apply_assignments(
        self,
        assignments: List[Tuple[Driver, Request]],
    ) -> None:
        """
        Assign requests to drivers.
        """
        for driver, req in assignments:
            if driver.status != "IDLE" or req.status != "WAITING":
                continue
            driver.assign_request(req, self.time)
            req.mark_assigned(driver.id)

    def _move_drivers_and_handle_events(self) -> None:
        """
        Move drivers and process pickup and dropoff events.
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

                reward = self._compute_earnings(req)
                d.earnings += reward

                d.current_request = None

    def _apply_mutations(self) -> None:
        """
        Apply mutation rules to all drivers.
        """
        for d in self.drivers:
            self.mutation_rule.maybe_mutate(d, self.time)

    def _compute_earnings(self, req: Request) -> float:
        """
        Compute earnings for a completed request.

        The earnings model is intentionally simple:
        a fixed base fee plus a distance-based component.

        Doctest
        -------
        >>> class P:
        ...     def __init__(self, x, y): self.x, self.y = x, y
        ...     def distance_to(self, other):
        ...         dx = self.x - other.x
        ...         dy = self.y - other.y
        ...         return (dx*dx + dy*dy) ** 0.5
        >>> class R:
        ...     def __init__(self):
        ...         self.pickup = P(0, 0)
        ...         self.dropoff = P(3, 4)
        >>> sim = DeliverySimulation([], None, None, None, 10, base_fee=10, distance_fee=1)
        >>> sim._compute_earnings(R())
        15.0
        """
        distance = req.pickup.distance_to(req.dropoff)
        return self.base_fee + self.distance_fee * distance

    def _avg_wait(self) -> float:
        """
        Compute the average waiting time of served requests.

        Doctest
        -------
        >>> sim = DeliverySimulation([], None, None, None, 10)
        >>> sim.wait_times = [2, 4, 6]
        >>> sim._avg_wait()
        4.0
        """
        if not self.wait_times:
            return 0.0
        return sum(self.wait_times) / len(self.wait_times)
