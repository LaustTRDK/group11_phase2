from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple


class DispatchPolicy(ABC):
    """
    Abstract base class for dispatch strategies.

    A DispatchPolicy proposes *offers* between drivers and requests.
    It MUST NOT modify drivers or requests directly.

    The returned list may contain multiple offers for the same request
    (this supports the Phase 2 idea where several drivers may receive
    the same offer and decide independently whether to accept).

    Concrete policies must implement `assign`.
    """

    @abstractmethod
    def assign(
        self,
        drivers: List["Driver"],
        requests: List["Request"],
        time: int,
    ) -> List[Tuple["Driver", "Request"]]:
        """
        Propose (driver, request) offers for the current tick.

        Parameters
        ----------
        drivers : list[Driver]
            All drivers in the system.
        requests : list[Request]
            All requests in the system.
        time : int
            Current simulation time.

        Returns
        -------
        list[(Driver, Request)]
            Proposed offers. No mutation is allowed.
        """
        raise NotImplementedError


class NearestNeighborOfferPolicy(DispatchPolicy):
    """
    Nearest-neighbour offer policy (Phase 2 style).

    For each WAITING request, offer it to the K nearest IDLE drivers.
    The same request may therefore be offered to multiple drivers.

    This policy is intentionally simple and pedagogical.

    Parameters
    ----------
    k : int
        Number of drivers to offer each request to.

    Doctest
    -------
    >>> class Point:
    ...     def __init__(self, x, y):
    ...         self.x, self.y = x, y
    ...     def distance_to(self, other):
    ...         dx = self.x - other.x
    ...         dy = self.y - other.y
    ...         return (dx*dx + dy*dy) ** 0.5
    ...
    >>> class Driver:
    ...     def __init__(self, id, x, y, status="IDLE"):
    ...         self.id = id
    ...         self.position = Point(x, y)
    ...         self.status = status
    ...
    >>> class Request:
    ...     def __init__(self, id, x, y, status="WAITING"):
    ...         self.id = id
    ...         self.pickup = Point(x, y)
    ...         self.status = status
    ...
    >>> d1 = Driver(1, 0, 0)
    >>> d2 = Driver(2, 5, 0)
    >>> d3 = Driver(3, 10, 0)
    >>> r = Request(99, 1, 0)
    >>> policy = NearestNeighborOfferPolicy(k=2)
    >>> offers = policy.assign([d1, d2, d3], [r], time=0)
    >>> len(offers)
    2
    >>> sorted(d.id for d, _ in offers)
    [1, 2]
    """

    def __init__(self, k: int = 1):
        self.k = max(1, int(k))

    def assign(
        self,
        drivers: List["Driver"],
        requests: List["Request"],
        time: int,
    ) -> List[Tuple["Driver", "Request"]]:

        offers: List[Tuple["Driver", "Request"]] = []

        idle_drivers = [d for d in drivers if getattr(d, "status", None) == "IDLE"]
        waiting_requests = [r for r in requests if getattr(r, "status", None) == "WAITING"]

        for req in waiting_requests:
            # sort idle drivers by distance to this request
            sorted_drivers = sorted(
                idle_drivers,
                key=lambda d: d.position.distance_to(req.pickup),
            )

            for d in sorted_drivers[: self.k]:
                offers.append((d, req))

        return offers


class GlobalGreedyOfferPolicy(DispatchPolicy):
    """
    Global greedy *offer* policy.

    Builds all (idle driver, waiting request) pairs, sorts them by distance,
    and proposes offers in increasing distance order.

    Unlike Phase 1, this policy does NOT enforce one-to-one matching.
    Conflict resolution is left to the simulation engine.

    This version avoids hashing Driver/Request objects directly and
    therefore works safely with dataclasses and mutable objects.

    Doctest
    -------
    >>> class Point:
    ...     def __init__(self, x, y):
    ...         self.x, self.y = x, y
    ...     def distance_to(self, other):
    ...         dx = self.x - other.x
    ...         dy = self.y - other.y
    ...         return (dx*dx + dy*dy) ** 0.5
    ...
    >>> class Driver:
    ...     def __init__(self, id, x, y, status="IDLE"):
    ...         self.id = id
    ...         self.position = Point(x, y)
    ...         self.status = status
    ...
    >>> class Request:
    ...     def __init__(self, id, x, y, status="WAITING"):
    ...         self.id = id
    ...         self.pickup = Point(x, y)
    ...         self.status = status
    ...
    >>> d1 = Driver(1, 0, 0)
    >>> d2 = Driver(2, 10, 0)
    >>> r1 = Request(1, 1, 0)
    >>> r2 = Request(2, 9, 0)
    >>> policy = GlobalGreedyOfferPolicy()
    >>> offers = policy.assign([d1, d2], [r1, r2], time=0)
    >>> len(offers)
    4
    """

    def assign(
        self,
        drivers: List["Driver"],
        requests: List["Request"],
        time: int,
    ) -> List[Tuple["Driver", "Request"]]:

        idle_drivers = [d for d in drivers if getattr(d, "status", None) == "IDLE"]
        waiting_requests = [r for r in requests if getattr(r, "status", None) == "WAITING"]

        pairs: List[Tuple[float, "Driver", "Request"]] = []

        for d in idle_drivers:
            for r in waiting_requests:
                dist = d.position.distance_to(r.pickup)
                pairs.append((dist, d, r))

        # sort globally by distance
        pairs.sort(key=lambda t: t[0])

        # return all offers (no mutation, no filtering)
        return [(d, r) for _, d, r in pairs]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
