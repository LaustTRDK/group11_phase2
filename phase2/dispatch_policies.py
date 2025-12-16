from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from .offer import Offer

if TYPE_CHECKING:
    from .driver import Driver
    from .request import Request


class DispatchPolicy(ABC):
    """
    Abstract base class for dispatch strategies.

    A dispatch policy proposes offers to drivers.
    It must not change drivers or requests directly.
    """

    @abstractmethod
    def assign(
        self,
        drivers: List["Driver"],
        requests: List["Request"],
        time: int,
    ) -> List[Offer]:
        """
        Return a list of offers for this time step.
        """
        raise NotImplementedError


class NearestNeighborPolicy(DispatchPolicy):
    """
    Offer each waiting request to nearby idle drivers.

    Each request is offered to the k nearest idle drivers.
    """

    def __init__(self, k: int = 3):
        """
        Create a nearest-neighbor policy.

        Parameters
        ----------
        k : int
            Number of drivers to offer each request to.
        """
        self.k = max(1, int(k))

    def assign(
        self,
        drivers: List["Driver"],
        requests: List["Request"],
        time: int,
    ) -> List[Offer]:
        """
        Create offers based on nearest idle drivers.

        --- DOCTEST ---
        >>> class P:
        ...     def __init__(self, x, y): self.x, self.y = x, y
        ...     def distance_to(self, o):
        ...         return ((self.x-o.x)**2 + (self.y-o.y)**2) ** 0.5
        >>> class D:
        ...     def __init__(self, i):
        ...         self.did = i
        ...         self.position = P(0, 0)
        ...         self.speed = 1.0
        ...         self.status = "IDLE"
        >>> class R:
        ...     def __init__(self):
        ...         self.pickup = P(1, 0)
        ...         self.status = "WAITING"
        >>> policy = NearestNeighborPolicy(k=1)
        >>> offers = policy.assign([D(1)], [R()], 0)
        >>> len(offers)
        1
        """
        idle = [d for d in drivers if getattr(d, "status", None) == "IDLE"]
        waiting = [r for r in requests if getattr(r, "status", None) == "WAITING"]

        offers: List[Offer] = []

        if not idle or not waiting:
            return offers

        for r in waiting:
            dists = [(d.position.distance_to(r.pickup), d) for d in idle]
            dists.sort(key=lambda t: t[0])

            for dist, d in dists[: self.k]:
                travel_time = dist / max(getattr(d, "speed", 1e-9), 1e-9)
                offers.append(
                    Offer(
                        driver=d,
                        request=r,
                        estimated_travel_time=travel_time,
                        estimated_reward=0.0,
                    )
                )

        return offers


class GlobalGreedyPolicy(DispatchPolicy):
    """
    Offer all (idle driver, waiting request) pairs.

    Pairs are sorted by distance.
    """

    def assign(
        self,
        drivers: List["Driver"],
        requests: List["Request"],
        time: int,
    ) -> List[Offer]:
        """
        Create offers for all driver-request pairs.

        --- DOCTEST ---
        >>> class P:
        ...     def __init__(self, x, y): self.x, self.y = x, y
        ...     def distance_to(self, o):
        ...         return abs(self.x - o.x)
        >>> class D:
        ...     def __init__(self):
        ...         self.did = 1
        ...         self.position = P(0, 0)
        ...         self.speed = 1.0
        ...         self.status = "IDLE"
        >>> class R:
        ...     def __init__(self):
        ...         self.pickup = P(2, 0)
        ...         self.status = "WAITING"
        >>> policy = GlobalGreedyPolicy()
        >>> offers = policy.assign([D()], [R()], 0)
        >>> len(offers)
        1
        """
        idle = [d for d in drivers if getattr(d, "status", None) == "IDLE"]
        waiting = [r for r in requests if getattr(r, "status", None) == "WAITING"]

        pairs = []
        for d in idle:
            for r in waiting:
                dist = d.position.distance_to(r.pickup)
                pairs.append((dist, d, r))

        pairs.sort(key=lambda t: t[0])

        offers: List[Offer] = []
        for dist, d, r in pairs:
            travel_time = dist / max(getattr(d, "speed", 1e-9), 1e-9)
            offers.append(
                Offer(
                    driver=d,
                    request=r,
                    estimated_travel_time=travel_time,
                    estimated_reward=0.0,
                )
            )

        return offers


if __name__ == "__main__":
    import doctest
    doctest.testmod()
