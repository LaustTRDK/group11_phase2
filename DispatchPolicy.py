from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple


class DispatchPolicy(ABC):
    """Abstract base class for all dispatch strategies.

    Subclasses must implement :meth:`assign`, which proposes pairs of
    (driver, request) objects without mutating them.

    The concrete ``Driver`` and ``Request`` types are not specified here;
    this module only assumes that:

    - a driver has at least ``status`` and ``position`` attributes, and
    - a request has at least ``status`` and ``pickup`` attributes.
    """

    @abstractmethod
    def assign(
        self,
        drivers: List["Driver"],
        requests: List["Request"],
        time: int,
    ) -> List[Tuple["Driver", "Request"]]:
        """Return a list of proposed (driver, request) pairs.

        Parameters
        ----------
        drivers:
            All drivers in the system.
        requests:
            All requests in the system.
        time:
            Current simulation time (tick). Included so that policies
            can use it if needed, even though the simple policies here
            ignore it.

        Returns
        -------
        list[(Driver, Request)]
            Suggested matches. The policy MUST NOT modify the driver
            or request objects; the simulation engine decides how to
            apply the proposals.
        """
        raise NotImplementedError


class NearestNeighborPolicy(DispatchPolicy):
    """Simple local matching strategy.

    Algorithm sketch
    ----------------
    1. Collect all *idle* drivers (status == ``"IDLE"``).
    2. Collect all *waiting* requests (status == ``"WAITING"``).
    3. While both lists are non-empty:
       a. Find the (driver, request) pair with the smallest distance
          between driver.position and request.pickup.
       b. Add that pair to the result.
       c. Remove the chosen driver and request from the candidate lists.

    This produces a greedy matching based only on the closest current pair.

    Doctest
    -------
    The example below uses tiny stand-in classes for ``Point``, ``Driver``
    and ``Request`` just to demonstrate the behaviour.

    >>> class Point:
    ...     def __init__(self, x, y):
    ...         self.x, self.y = x, y
    ...     def distance_to(self, other: "Point") -> float:
    ...         dx = self.x - other.x
    ...         dy = self.y - other.y
    ...         return (dx * dx + dy * dy) ** 0.5
    ...
    >>> class Request:
    ...     def __init__(self, pickup, status="WAITING"):
    ...         self.pickup = pickup
    ...         self.status = status
    ...
    >>> class Driver:
    ...     def __init__(self, position, status="IDLE"):
    ...         self.position = position
    ...         self.status = status
    ...
    >>> d1 = Driver(Point(0, 0))      # closer to r
    >>> d2 = Driver(Point(10, 0))
    >>> r = Request(Point(1, 0))
    >>> policy = NearestNeighborPolicy()
    >>> pairs = policy.assign([d1, d2], [r], time=0)
    >>> len(pairs)
    1
    >>> pairs[0][0] is d1  # nearest driver was chosen
    True
    >>> pairs[0][1] is r
    True
    """

    def assign(
        self,
        drivers: List["Driver"],
        requests: List["Request"],
        time: int,
    ) -> List[Tuple["Driver", "Request"]]:

        matches: List[Tuple["Driver", "Request"]] = []

        # 1) All idle drivers
        idle_drivers = [d for d in drivers if getattr(d, "status", None) == "IDLE"]

        # 2) All waiting requests
        waiting_reqs = [r for r in requests if getattr(r, "status", None) == "WAITING"]

        # 3) Greedily match nearest pairs until one list is exhausted
        while idle_drivers and waiting_reqs:
            best_pair: Tuple["Driver", "Request"] | None = None
            best_distance = float("inf")

            # Find nearest (driver, request) pair
            for d in idle_drivers:
                for r in waiting_reqs:
                    dist = d.position.distance_to(r.pickup)
                    if dist < best_distance:
                        best_distance = dist
                        best_pair = (d, r)

            if best_pair is None:
                break

            matches.append(best_pair)

            # Remove chosen driver and request from consideration
            driver, req = best_pair
            idle_drivers.remove(driver)
            waiting_reqs.remove(req)

        return matches


if __name__ == "__main__":
    import doctest

    doctest.testmod()
