from __future__ import annotations
from abc import ABC, abstractmethod
from .driver import Driver
from .driver_behaviour import (
    GreedyDistanceBehaviour,
    EarningsMaxBehaviour,
    LazyBehaviour,
    Naive
)
import random

class MutationThresholds:
    """This class purpose is to be a object holder for all mutations thresholds.
    thr = threshold. 

    lasttime_mutation_thr : is just a max time limit. = 30
    expire_thr: is just a max = 3 
    earning_thr: ratio = 0.25 (same logic as earnings behavior calculations)
    and says for one expirations window of time they shold have earned at least 5
    accepted_thr: ratio 0.05 -> so that they have accepted at leat one 
    request pr expire window
    
    OBS: Enten skal vi bruge:
    threshold = mutationsthresholds(
        lasttime_mutation_thr = værdi,
        expire_thr = værdi,
        earning_thr = værdi,
        accepted_thr = værdi
    )
    eller også skal vi i denne sætte dem lig med en defoult og så kan man i anden
    del af koden ændre på tingene. 
    """
    def __init__(
            self,
            lasttime_mutation_thr: int = 30, # thr for random (max)
            expire_thr: int = 3, # thr for amount of expired request since last mutation (max)
            earning_thr: float = 0.25, # thr for amount earnings last mutation (min)
            accepted_thr: float = 0.05 # thr for amount accepted request since last mutation (min)
    ) -> None:
        self.lasttime_mutation_thr = lasttime_mutation_thr
        self.expire_thr = expire_thr
        self.earning_thr = earning_thr
        self.accepted_thr = accepted_thr

class MutationRule(ABC):
    """This is the parent class / base class to all the mutations rules.

    """
    def maybe_mutate(self, driver: Driver, time: int) -> None:
        """Return true if the driver should mutate / will mutate and False
        otherwise. Right now there is only one rule"""
        raise NotImplementedError
    
class DecisionTreeRule(MutationRule):
    """This mutation rule will follow a decision tree. 
    
    This rule is a disition tree based that works a little on
    preformance and a little on randomness. 
    There is a threshold for how long since last mutation before it will
    mutate to a random behavior. 
    Then it will look at:
    
    OBS: hvis jeg ikke ændre det til det der står i punkterne så skal jeg have ændret det til det er threshold bestemt antal af følgnede
        A) If the amount of expired request since last mutation has supased athreshold
        B) If the amount of earnings since last mutation is below a threshold
        C) If the amount of accepted requests since last mutation is below a threshold

    Then based on witch one that returns true and if there is a combination of 
    more than one of the A, B and C that turns true. On a desision tree based way
    it will implement eighter: 
        - Greedy behavior
        - Earning behavior
        - Lasy hebavior
        - Lasy hebavior
        - Random = takes a ramdon behavior from the options above
    """
    def __init__(self, thresholds: MutationThresholds) -> None:
        self.thresholds = thresholds

    @staticmethod
    def _random_behaviour():
        return random.choice([
            GreedyDistanceBehaviour,
            EarningsMaxBehaviour,
            LazyBehaviour,
            Naive
        ])

    def maybe_mutate(self, driver: Driver, time: int) -> None:
        """Earmings calculation follows same logic as the calculation of the ratio in
        the earnings behavior class (ratio = total eanings / timepeiot)
        """
        # ------- mutation based on time since last mutation ------------
        time_since_last = time - driver.behaviour_mutation_stamp
        if time_since_last >= self.thresholds.lasttime_mutation_thr:
            driver.update_behaviour_and_stamp(time, self._random_behaviour())
            return
        
        # ------- collect infomation based on reasent history ------------
        events = driver.all_events_since_last_mutation()

        expired = sum(1 for ev in events if ev.event == "expired")
        earnings_ratio = (sum(ev.earnings for ev in events if ev.event == "DELIVERED" and ev.earnings is not None)) / time_since_last
        accepted_ratio = (sum(1 for ev in events if ev.event == "accepted")) / time_since_last

        # ------- check threshold ------------
        A = expired >= self.thresholds.expire_thr
        B = earnings_ratio < self.thresholds.earning_thr
        C = accepted_ratio < self.thresholds.accepted_thr

        if not (A or B or C):
            return  # if not threshold is reached then nothing happens

        # ------- mutation based on on reasent history ------------
        current_behaviour = driver.behaviour
        GreedyBe = GreedyDistanceBehaviour
        EarningBe = EarningsMaxBehaviour
        LasyBe = LazyBehaviour
        NaiveBe = Naive

        if A and not B and not C:
            driver.behaviour = GreedyBe() if type(current_behaviour) != GreedyBe else LasyBe()

        elif B and not A and not C:
            driver.behaviour = EarningBe() if type(current_behaviour) != EarningBe else GreedyBe()
        
        elif C and not A and not B:
            driver.behaviour = NaiveBe() if type(current_behaviour) != NaiveBe else EarningBe()

        elif A and B and not C:
            driver.behaviour = GreedyBe() if type(current_behaviour) != GreedyBe else self._random_behaviour()()

        elif B and C and not A:
            driver.behaviour = EarningBe() if type(current_behaviour) != EarningBe else NaiveBe()

        elif A and C and not B:
            driver.behaviour = LasyBe() if type(current_behaviour) != LasyBe else self._random_behaviour()()

        elif A and B and C:
            driver.behaviour = self._random_behaviour()()

        # ------- Update mutation timestamp on driver ------------
        driver.behaviour_mutation_stamp = time