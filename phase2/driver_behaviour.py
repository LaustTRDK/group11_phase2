from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from phase2 import offer

if TYPE_CHECKING:
    from .driver import Driver
    
from .offer import Offer


class DriverBehaviour(ABC):
    """This class is to set the ground for different driver beheveour and how it can
    react to request offers. So it is set to accept or decline request offers on 
    the grounds of what behavior that the driver have an though the subclass 
    behaviour the logic that is basis of their desisions lays. 

    This class do not have to have a "__init__" becouse it is a abstract class that do
    not store any data, nor initilize anything. This is not an object but a contract 
    to how drivers will / can behave.

    To implement the behaviour the Strategy pattern is chosen to be used. 

    This class implement a rule taht all classes that it is a parrent to have to 
    have a method implemented that is named deside. So all subclasses under it 
    will include a such method. 

    This is a abstrack class thtat have no methods but only defines the methods that
    class will support. The methods is implem,enteted in derived classes. 
    """
    def decide(self, driver: Driver, offer: Offer, time: int) -> bool:
        """This will return True if the driver accepts the offer of the request, Flase
        otherwise.
        254
        State pattern
        """
        raise NotImplementedError

class GreedyDistanceBehaviour(DriverBehaviour):
    """This subclass to the driverbehaviour class decribes the behaviour for accepting
    or declinging requests by the logic:
        Accepting the request if the distance to the pickup is below a given threshold.

    Every request will expire if the after creation the request have been active for 
    20 ticks. 

    In contrast to this the driver vill first calculate what is the max distance the
    driver can acomplice in contrast to its speed before a newly produced request 
    will expire. Then it will take a third of this distance and this is the max 
    distance to the pickup for the offereed request. 
    Pros: all drivers will share the max expire time that they all will calculate
    from. Faster drivers will just cover a greater distance for what they will 
    accept. Therefore all drivers will also disregard long time pickups that will
    leave them with much less time to do the pickup. 
    Cons: that the faster drivers will be willing to accept very far-away pickups in
    contrast to slower drivers and hence more unpaid tracel. And slow drivers can 
    decline a lot of jobs becouse it is to far and therefore stave them. To conter-
    act a little the problem of witch the unknown of the dropoff distance I will also
    set a cap of the distance from the pickup to the dropof so that they do not accept
    something that has a distance from pickup to dropoff that are the same amount
    or above that of their max_distance. 

    The max distance if not anything is given by the system then will calculate it
    and use the calculation for the validation of accept or not accept. 

    """
    def __init__(self, expiretime: int = 20, max_distance: float = 0.0):
        self.max_distance = max_distance
        self.expiretime = expiretime

    def decide(self, driver: Driver, offer: Offer, time: int) -> bool:
        if self.max_distance == 0:
            self.max_distance = driver.speed * self.expiretime

        max_distance_to_pickup = self.max_distance / 3
        pick_dist = driver.position.distance_to(offer.request.pickup)
        drop_dist = offer.request.pickup.distance_to(offer.request.dropoff)

        if pick_dist <= max_distance_to_pickup and drop_dist <= self.max_distance:
            return True
        return False
   
    


class EarningsMaxBehaviour(DriverBehaviour):
    """This subclass to the driverbehaviour class decribes the behaviour for accepting
    or declinging requests by the logic:
        Accepting the request if the ratio estimated reward divided by travel time
        is above a threshold. 

    The earnings is 5 for a order delivered given that a normal delivery have a distance
    of 5. After the first initial distance of 5 then the driver will recive +=1 for 
    every 5 distance above the initial 5 distance. 
    total distance = pickup_distance + dropoff_distance
    earning_distancde = total_distance - 5
    expected_earning = 5 + (earnings_distance / 5)
    trip_time = total_distance / driver_speed
    ratio = expected_earning / trip_time 

    I have set a min_ratio at 0.3 as defaoult but that it can be changed if so
    desired by the operator or other parts of the simulation code. 

    The driver will acept a request if the self_calculated ratio is above or equal to 
    that of the min_ratio. 

    Man kunne have lavet en anden klasse der fortæller om reference job og beregner
    en ratio for en reference job. Derefter sammenligne med reference hvor driver kun 
    acceptere noget der er mindst 60-80% så godt. Denne er god hvis man ændre på hvor
    meget at de kan tjene senere så passer koden stadig ret godt men det betyder også
    at det hele afhænger af de specefikke referencde parametre som sættes op for 
    reference beregningen hvilket kan give et bias system hvis denne reference ikke er
    repræsentativ for systeemet. 
    Sammenligningen sker via beregningne: 
    threshold = parameter * ratio_reference
    paramter på: 
        * parameter = 1.0 : acceptere kun jobs der er lige så gode som referencen
        * parameter < 1.0 : acceptere jobs der er dårligere end referencen ned til 
        til bestemte fraktion
        * parameter > 1.0 : acceptere kun jobs der er bedre end referencen. 
    Hvis man endda sætter en form for "scaæe" for paramteret så det acceptere jobs der
    er parameter = 0.5 eller højere. Så vil driver acceptere jobs der også er middel-
    mådige men ikke alt for dårlige. Mens hvis parameteret er parameter 0.9 og op så 
    betyder det at de kun acceptere jobs der er meget tæt på eller bedre end 
    referencen. fx. 
    - denne metode skulle jeg så have lavet en anden klasse eller method der beregner
    reference ratio så den kunne bruges her. 
    """
    def __init__(self, min_ratio: float = 0.3):
        self.min_ratio = min_ratio
        
    def decide(self, driver: Driver, offer: Offer, time: int) -> bool:
        driver_to_pickup_dist = driver.position.distance_to(offer.request.pickup)
        pickup_to_dropoff_dist = offer.request.pickup.distance_to(offer.request.dropoff)
        total_distance = driver_to_pickup_dist + pickup_to_dropoff_dist
        earning_distancde = total_distance - 5 
        expected_earning = 5 + (earning_distancde // 5)
        trip_time = total_distance / driver.speed
        driver_ratio = expected_earning / trip_time
        if driver_ratio >= self.min_ratio:
            return True
        else: 
            return False


class LazyBehaviour(DriverBehaviour):
    """"This subclass to the driverbehaviour class decribes the behaviour for accepting
    or declinging requests by the logic:
        Accepting the request if and only if the request is close and the driver has
        been idle for longer than a configurable number of ticks. 

    OBS: max_idle_time er nok lidt lav
    """
    def __init__(self, close = 5, max_idle_time = 6):
        """This class have been given a defoult value for the distance for when a 
        driver consider the pickup pace to be close by and the defoult value of 
        max time the driver can be idle before it have to take on a request. 

        If not anything else is given the defould values is used in the validation 
        of if the driver will accept or not the request. 
        """
        self.close = close
        self.max_idle_time = max_idle_time

    def decide(self, driver: Driver, offer: Offer, time: int) -> bool:
        """This is the part that evaluate if the request offer allign with the
        behavior of the driver
        """
        idle_time = driver.idle_time
        distance_to_pickup = driver.position.distance_to(offer.request.pickup)
        if distance_to_pickup <= self.close and idle_time >= self.max_idle_time:
            return True
        else:
            return False
        

class Naive(DriverBehaviour):
    """This behavior accepts ALL!"""
    def decide(self, driver, offer, time):
        return True