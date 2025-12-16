from __future__ import annotations
import numpy, os, decorator, math
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple
from collections import deque
from abc import ABC, abstractmethod
import random

# Core Domain Classes

#----------------------------------------------------------------------------#
#     Point classes
#----------------------------------------------------------------------------#

class Point:
    """This class contains the structure of an Point and the methods that describe its functionality. 
    A point is in 2D and therefore contains a x-coordinat and an y-coordinat. Thease two coordinaes,
    can not have a negative value and be inside the grid. 

    The grid for the simulation have a width of 50.0 and a height of 30.0. Therefor can the 
    coordinates for the Point not be higher than the grid. This means that the x-coordinat,
    can not have a higher value than 50.0 and the y-coordinat can not have a higher value of 
    30.0. The constand of the grid size are defined as the first thing in this class in order
    to make it more easy to change if neede later. 
    """
    # Grid size constants
    GRID_WIDTH = 50.0
    GRID_HEIGHT = 30.0

    def __init__(self, x = 0.0, y = 0.0) -> None:
        """This is the main part of the class and decribes the objects of the class. 
        It also validate the input if the object added are acceptable for the class to make a Point. 
        If the values of the added objects is not accepted then it will raise a value error. 
        Objects for this class can not be of negative values and have to be inside of the limits of the
        grid of the future simulation. 

        The simulations grid have a grid width at 50.0 and reprecents the x coordinat and the grid
        height have a max at 30.0 and reprecents the y coordinat. 
        The objects values have to be eitghter a integer or an float where no other types will be 
        accepted. 

        To valuate the values of the added objects for this class the method of is_valid is used. 

        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> print(q)
        3, 3
        """
        if self.is_valid(x, y):
            self.x = x
            self.y = y
        else:
            raise ValueError("Invalid value for Point")

    @staticmethod
    def is_valid(x: float = 0.0, y: float = 0.0) -> bool:
        """This method is used to validate the values for a poteintal Point. So that no point with a
        not valid value will be made. This method validate that the values to be made into a Point
        is eighter a intger or an float and that the value lay insde the parameters of the simulation
        grid.  
        """
        # type tjeck
        if not isinstance(x, (int, float)):
            return False
        if not isinstance(y, (int, float)):
            return False
        
        # Tjeck coordinats are inside the boundary of the grid
        if not (x >= 0.0 and x <= Point.GRID_WIDTH):
            return False
        if not (y >= 0.0 and y <= Point.GRID_HEIGHT):
            return False
        
        return True
    
    def distance_to(self, other: Point) -> float:
        """This method returns the Euclidean distance between this point and another.
        This is based on: 
        sqrt((x1 - x2)**2 + (y1 - y2)**2 

        This calculates the distance between two points. Both values have to be of the 
        Point class and if they are not there will be raised an value error. 

        >>> p = Point()
        >>> p.set_point(0, 0)
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> p.distance_to(q)
        4.242640687119285
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        # Anden måde at gøre det på nedenunder: er ikke sikker på at jeg faktisk må gøre det på den måde
        ## return math.hypot(self.x - other.x, self.y - other.y)
        # Hvis jeg ikke må bruge math.hypo() så brug nedestående. 
        ## return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def get_point(self) -> tuple[float, float]:
        """This method gives the point returned. 

        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q.get_point()
        (3, 3)

        If the object in question is not a Point that do not have negative values, 
        there will be raised an error. 
        """
        return (self.x, self.y)
    
    def set_point(self, x: float, y:float) -> None:
        """This method will set a point from the values given.

        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q.get_point()
        (3, 3)

        If the object in question is not a Point that do not have negative values, 
        there will be raised an error.
        """
        if self.is_valid(x, y):
            self.x = x
            self.y = y
            return self
    
    def __str__(self) -> str:
        """This method is to give a string representation of the Point in question. 
        So this returns a string representation of the Point. 

        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> print(q)
        3, 3
        
        If the object in question is not a Point then it will not be printets as so, 
        and then it will be returned according to the rules of that paticular 
        objects class 
        """
        return f"{self.x}, {self.y}"
    
    def __repr__(self) -> str:
        """This method are to return a representation of a Point, so the returned is 
        numerica and can be used in other methods sofouth.
        """
        return f"Point({self.x}, {self.y})"

    def copy_point(self):
        """This method is to copy the point for the further use. 
        
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q.copy_point()
        Point(3, 3)

        The object in question have to be of the Point class. 
        """
        return Point(self.x, self.y)
    
    def __add__(self, other: any) -> Point:
        """This method allow the Point to have another point added to the value of
        its coordinates or to add a value to both coordinates of a point depending on
        if the object other is of the class Point, int or float. 
        If the object of other is a Point then the point coordinates of other is added
        to the Point in question, so that the x coordinat for other is added to the x 
        coordinate of the Point in question. The same goes for the y coordinate. 
        If the object of other is eighter an intgeger or an float then that value will be
        added to both the x and y coordinate of the Point in question. 
        If the object of other is anything else than eitghter a Point, integer or a float
        then there will be rasied an error. 

        This method returns a point. 

        Docktest when other is a Point:
        >>> p = Point()
        >>> p.set_point(2, 2)
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> r = p + q
        >>> print(r)
        5, 5

        Dockterst when other is an int:
        >>> p = 2
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> r = p + q
        >>> print(r)
        5, 5

        Dockterst when other is an float:
        >>> p = 2.5
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> r = p + q
        >>> print(r)
        5.5, 5.5
        """
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif type(other) in (int, float) and other >= 0.0:
            return Point(self.x + other, self.y + other)
        else: 
            raise ValueError("The object of other is not of the type of Point, integer or an float")
        
    
    def __sub__(self, other: Point) -> Point:
        """This method allow the Point to have another point substracted to the value of
        its coordinates or to substract a value to both coordinates of a point depending on
        if the object other is of the class Point, int or float. 
        If the object of other is a Point then the point coordinates of other is substracted
        to the Point in question, so that the x coordinat for other is substracted to the x 
        coordinate of the Point in question. The same goes for the y coordinate. 
        If the object of other is eighter an intgeger or an float then that value will be
        substracted to both the x and y coordinate of the Point in question. 
        If the object of other is anything else than eitghter a Point, integer or a float
        then there will be rasied an error. 

        This method returns a point. 

        Docktest when other is a Point:
        >>> p = Point()
        >>> p.set_point(2, 2)
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> r = q - p
        >>> print(r)
        1, 1
        

        Dockterst when other is an int:
        >>> p = 2
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> r = q - p
        >>> print(r)
        1, 1

        Dockterst when other is an float:
        >>> p = 2.5
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> r = q - p
        >>> print(r)
        0.5, 0.5
        """
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        elif type(other) in (int, float) and other >= 0.0:
            return Point(self.x - other, self.y - other)
        else: 
            raise ValueError("The object of other is not of the type of Point, integer or an float")
        
    
    def __iadd__(self, other: Point) -> Point:
        """This method allow the Point to have another point added to the value of
        its coordinates or to add a value to both coordinates of a point depending on
        if the object other is of the class Point, int or float. 
        This method of adding is when using the += way of adding one value to anoter. 
        If the object of other is a Point then the point coordinates of other is added
        to the Point in question, so that the x coordinat for other is added to the x 
        coordinate of the Point in question. The same goes for the y coordinate. 
        If the object of other is eighter an intgeger or an float then that value will be
        added to both the x and y coordinate of the Point in question. 
        If the object of other is anything else than eitghter a Point, integer or a float
        then there will be rasied an error. 

        This method returns a point. 

        Docktest when other is a Point:
        >>> p = Point()
        >>> p.set_point(2, 2)
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q += p
        5, 5

        Dockterst when other is an int:
        >>> p = 2
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q += p
        >>> print(q)
        5, 5

        Dockterst when other is an float:
        >>> p = 2.5
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q += p
        >>> print(q)
        5.5, 5.5
        """
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
            return self
        elif type(other) in (int, float) and other >= 0.0:
            self.x += other
            self.y += other
            return self
        else:
            raise ValueError("The object of other is not of the type of Point, integer or an float")

    def __isub__(self, other: Point) -> Point:
        """This method allow the Point to have another point substracted to the value of
        its coordinates or to substract a value to both coordinates of a point depending on
        if the object other is of the class Point, int or float. 
        This method of sybstracting is when using the -= way of sybstracting one value to anoter.
        If the object of other is a Point then the point coordinates of other is substracted
        to the Point in question, so that the x coordinat for other is substracted to the x 
        coordinate of the Point in question. The same goes for the y coordinate. 
        If the object of other is eighter an intgeger or an float then that value will be
        substracted to both the x and y coordinate of the Point in question. 
        If the object of other is anything else than eitghter a Point, integer or a float
        then there will be rasied an error. 

        This method returns a point. 

        Docktest when other is a Point:
        >>> p = Point()
        >>> p.set_point(2, 2)
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q -= p
        1, 1

        Dockterst when other is an int:
        >>> p = 2
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q -= p
        >>> print(q)
        1, 1

        Dockterst when other is an float:
        >>> p = 2.5
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q -= p
        >>> print(q)
        0.5, 0.5
        """
        if isinstance(other, Point):
            self.x -= other.x
            self.y -= other.y
            return self
        elif type(other) in (int, float) and other >= 0.0:
            self.x -= other
            self.y -= other
            return self
        else:
            raise ValueError("The object of other is not of the type of Point, integer or an float")

    def __mul__(self, other: Any):
        """This method is able to multiply a point with another point or a point with a value of the
        type of integer or an float. If it is a point multiplyed with another point then it is the 
        x coordinate multiplied with the other x coordinate. Likewise for the y coordinates. 
        If it is the case og multiplying a point with a value of the type integer or float then both 
        the x and y coordinate of the point will be multiplied with the value. 
        If the value of the object other is eighter a Point, integer or an float then there will be 
        raised an error. 
        
        This method returns a point. 

        Docktest when other is a Point:
        >>> p = Point()
        >>> p.set_point(2, 2)
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q *= p
        6, 6

        Dockterst when other is an int:
        >>> p = 2
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q -= p
        >>> print(q)
        6, 6
        

        Dockterst when other is an float:
        >>> p = 2.5
        >>> q = Point()
        >>> q.set_point(3, 3)
        >>> q -= p
        >>> print(q)
        7.5, 7.5
        """
        if isinstance(other, Point):
            self.x *= other.x
            self.y *= other.x
            return self
        elif type(other) in (int, float) and other >= 0.0:
            self.x *= other
            self.y *= other
            return self
        else: 
            raise ValueError("The inserted value are not one of tree accepted types: An integer, a float or a Point")
            
    __rmul__ = __mul__
    """The method of __mul__ is the same as __rmul__. They will work the same."""

#----------------------------------------------------------------------------#
#     Request classes
#----------------------------------------------------------------------------#

class request:
    """This reprecents a single food-delivery request with pickup and dropoff locations
    
    Some of the atributes are optional. When some are optional and some will be changed depending on the request.   

    The objects for this class is as follows: 
    * rid: is the request id. This is an integer of 1 and up. Where 0 is a palceholder for before 
    the request is created. 
    * pickup: is the Point on the grid where the request have to be picked up from the resurent. 
    So to pickup Point is equlient to a adress of the resurent. 
    * dropoff: IS the point on the grid where the request have to be delivered to. The custumor, witch
    make the dropoff point equlient to the adress of the customer. 
    * creation_time: Is the time for when the request was made. So when it come to excist. 
    * status: Is the status of the request. This can be changed whougout time as actions for
    compleating the order/request is progressing. It can be one of folloing: ("WAITING", "ASSIGNED", "PICKED", "DELIVERED", "EXPIRED")
    * assigned_driver_id: IS the id of the driver that accepted the request and if the request got
    expired so the id of the driver that failed. 

    The wait_time -> I think it shall count 2 times. One from accepted request to the driver have picked the order up,
    and one from the driver have picked the order up to it has been delivered. 
    The two times put together will mark the entire time that the request have spend in the system.

    There is five wait time slots:
    * Wait_time is the current time. 
    * pickup_wait_time is the calculated time that took a driver to pickup the request after its creation.
    * delivered_wait_time it the calculated time that took a driver from pickup time to the order has been
    delivered. 
    * expired_wait_time it the calculated time from request created to the request got expired. This part
    is more in order to validate that all the requests that expire do not expire before the set expireation
    time. 

    OBS: vi skal have noget det tjekker for at alle expired_wait_time er ens og er den tid for vi har valgt
    at orderer udløber. 
    

    NOTER
    : Når en request bliver produceret / lavet så skal den ændre på 
    self.creation_time til at være til den tid hvor den blev lavet. 
    Men hvor i koden dette skal gøres??? 
    : Samt skal der måske i stedet for self.wait_time være både en pickup_wait_time,
    delivered_wait_time og en expired_wait_time??? 
    : Hvor i vores kode skal der stå at den ikke længere skal opdatere 
    på request wait_time når den er blevet leveret/ expired? 
    : Når/ hvis ordreren er delivered eller expired skal så assigned_driver_id fjernes fra ordreren? I forhold til at dette ikke skal stå i vejen for at driver kan påtage en ny ordre. -> må gerne forblive
    """
    def __init__(self, rid: int, pickup: Point, dropoff: Point, creation_time: int = 0, status: str = "WAITING", assigned_driver_id: int = 0, wait_time: int = 0, pickup_wait_time: int = 0, delivered_wait_time: int = 0, expired_wait_time: int = 0):
        """This method is the initial method that specefic the objects for this class. For this
        it uses the is_valid to validate the input objects to evaluate if they are of the rigtig
        data types and is in bounds with the values that make sence for a request. 
        If the values of the objects is not accepble then there will be raised an error. 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)

        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )

        >>> print(r)
        id: 1,
        pickup: 0, 0,
        dropoff: 20, 10,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0

        """
        if self.is_valid(rid, pickup, dropoff, creation_time, status, assigned_driver_id, wait_time, pickup_wait_time, delivered_wait_time, expired_wait_time):
            self.rid = rid
            self.pickup = pickup
            self.dropoff = dropoff
            self.creation_time = creation_time
            self.status = status
            self.assigned_driver_id = assigned_driver_id
            self.wait_time = wait_time
            self.pickup_wait_time = pickup_wait_time
            self.delivered_wait_time = delivered_wait_time
            self.expired_wait_time = expired_wait_time
        else:
            raise ValueError("invalid value for one of the request attributes values")
    
    @staticmethod
    def is_valid(rid, pickup, dropoff, creation_time, status, assigned_driver_id, wait_time, pickup_wait_time, delivered_wait_time, expired_wait_time) -> bool:
        """This method is to validate the atributes there are in __init__. This valueates the objects
        is acceptable for the type class. 
        """
        if not isinstance(rid, int) or rid < 0:
            return False
        if not isinstance(pickup, Point):
            return False
        if not isinstance(dropoff, Point):
            return False
        if not isinstance(creation_time, int) or creation_time < 0:
            return False
        if status not in ("WAITING", "ASSIGNED", "PICKED", "DELIVERED", "EXPIRED"):
            return False
        if assigned_driver_id is not None and not isinstance(assigned_driver_id, int) or assigned_driver_id < 0:
            return False
        if not isinstance(wait_time, int) or wait_time < 0:
            return False
        if not isinstance(pickup_wait_time, int) or pickup_wait_time < 0:
            return False
        if not isinstance(delivered_wait_time, int) or delivered_wait_time < 0:
            return False
        if not isinstance(expired_wait_time, int) or expired_wait_time < 0:
            return False
        
        return True

    def update_creation_time(self, t: int) -> None:
        """This method have to change the creation time when the request is given.
        This means that this time have to be added / updated when the request,
        is created and thereafter will be constant for the rest of the request
        running time for that specefic request id. 

        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)

        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )

        >>> print(r)
        id: 1,
        pickup: 0, 0,
        dropoff: 20, 10,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 0

        >>> timetest = 2
        >>> r.update_creation_time(timetest)
        >>> print(r)
        id: 1,
        pickup: 0, 0,
        dropoff: 20, 10,
        creation_time: 2,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0
        """
        self.creation_time = t
    
    def is_active(self) -> bool:
        """Returns True if the request is still waiting, assigned, or picked 
        (that is, not delivered or expired).
        If it is delivered or expired then it will return False and if it is something entirly else
        then it will raise an error becouse it should not be able to be anything else than those 
        listet. 

        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)

        If the request is active: 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.is_active()
        True

        If the request is not active: 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "DELIVERED",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.is_active()
        False
        """
        if self.status in ("WAITING", "ASSIGNED", "PICKED"):
            return True
        elif self.status in ("DELIVERED", "EXPIRED"):
            return False
        else:
            raise ValueError("There have been an major error to the status, so that is something it should not be able to be")
        
    def mark_assigned(self, driver_id: int) -> None:
        """This will mark / assign a driver_id to the request. 
        This method will make it posible to assign a driver_id to a request or change it. 

        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.mark_assigned(driveridtest)
        >>> print(r)
        id: 1,
        pickup: 0, 0,
        dropoff: 20, 10,
        creation_time: 0,
        status: ASSIGNED,
        assigned_driver_id: 3,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 0
        
        : Det kan være der skal være en if: i forhold til accepted eller ej ellers også så skal det være et andet sted. -> altså hvis driver accepts the request and first then the assigned_driver_id can be changed.-> nej hvis driver accepter skal den bare kalde på denne
        """
        self.status = "ASSIGNED"
        self.assigned_driver_id = driver_id

    def mark_picked(self, t: int) -> None:
        """This method shall change the status to picked and set the wait_time to zero again.
        Then also return the time for when this happend (so that anoter part of the code can use this).
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> timetest = 2
        >>> r.mark_picked(timetest)
        >>> print(r)
        id: 1,
        id: 1,
        pickup: 0, 0,
        dropoff: 20, 10,
        creation_time: 0,
        status: PICKED,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 2,
        delivered_wait_time: 0,
        expired_wait_time: 0
        """
        self.status = "PICKED"
        self.pickup_wait_time = t - self.creation_time

    
    def mark_delivered(self, t: int) -> None:
        """This method have to mark the request as delivered. And at the same time add the infomation
        abut what the delivered_wait_time is. 

        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> timetest = 4
        >>> r.mark_delivered(timetest)
        >>> print(r)
        id: 1,
        pickup: 0, 0,
        dropoff: 20, 10,
        creation_time: 0,
        status: DELIVERED,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 4,
        expired_wait_time: 0

        OBS: How long it took the driver to deliver the request is this time,
        should there be a return for the statistic futher down the code???
        """
        self.status = "DELIVERED"
        self.delivered_wait_time = ((t - self.creation_time) - self.pickup_wait_time)


    def mark_expired(self, t: int) -> None:
        """Thuis method have to mark the request as expired.And at the same time add the infomation
        abut what the delivered_wait_time is. 
        

        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> timetest = 6
        >>> r.mark_delivered(timetest)
        >>> print(r)
        id: 1,
        pickup: 0, 0,
        dropoff: 20, 10,
        creation_time: 0,
        status: EXPIRED,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 6
        """
        #Opffange hvilken status ordreren var nået til da ordreren expired)?
        self.status = "EXPIRED"
        self.expired_wait_time = t - self.creation_time

    def update_wait(self, current_time: int) -> None:
        """Updates wait_time according to current_time.
        
        This method have to update the wait time to that of the current time.
        This skould be done whenever the status changes or?????????????????????????????????

        OBS: hvor i koden står der hvor denne starter? 
        OBS: hvor i koden står der at denne skal stoppe? 
        OBS: hvor tit bliver denne opdateret? Fordi det kommer an på 
        hvordan at wait_time skal håndteres med metods. 
        skal den opdateres fra et andet sted? I forhold til hvordan koden bestemmer hvornår at hver enkelt
        returest expires???? 
        """
        self.wait_time = current_time - self.creation_time
    
    def __str__(self) -> str:
        """This method is specefi how the code will reprecent the class object as an string."""
        return f"id: {self.rid},\n pickup: {self.pickup},\n dropoff: {self.dropoff},\n creation_time: {self.creation_time},\n status: {self.status},\n assigned_driver_id: {self.assigned_driver_id},\n wait_time: {self.wait_time}, \n pickup_wait_time: {self.pickup_wait_time},\n delivered_wait_time: {self.delivered_wait_time},\n expired_wait_time: {self.expired_wait_time}"
    
    def __repr__(self):
        """RThis method are to return a representation of a request, so the returned is 
        numerica and can be used in other methods sofouth.
        """
        return f"request(id = {self.rid}, pickup = {self.pickup}, dropoff = {self.dropoff}, creation_time = {self.creation_time}, status = {self.status}, assigned_driver_id = {self.assigned_driver_id}, wait_time = {self.wait_time}, pickup_wait_time = {self.pickup_wait_time}, delivered_wait_time = {self.delivered_wait_time}, expired_wait_time = {self.expired_wait_time})" 

    def copy_request(self):
        """This method make it posible to copy the request for other functions.
        """
        return request(self.rid, self.pickup, self.dropoff, self.creation_time, self.wait_time, self.assigned_driver_id, self.wait_time)
    
    # Getters : there will be a getter for everey object in the request
    #def get_request(self, ):
        #"""This method is right now a placeholder for if needed then there should be a method for getting
        #the whole request. 
        #"""
    
    def get_request_rid(self):
        """This method is to get the info about the request id
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_rid()
        1
        """
        return self.rid
    def get_request_pickup(self):
        """This method is to get the information abut the request picup point
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_pickup()
        Point(0, 0)
        """
        return self.pickup
    def get_request_dropoff(self):
        """This method is to get the information abut the request dropoff point
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_dropoff()
        Point(20, 10)
        """
        return self.dropoff
    def get_request_creation_time(self):
        """This method is to get the information abut the request creation_time.
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_creation_time()
        0
        """
        return self.creation_time
    def get_request_status(self):
        """This method is to get the information abut the request status.
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_status()
        'WAITING'
        """
        return self.status
    def get_request_assigned_driver_id(self):
        """This method is to get the information abut the requests assigned drivers id.
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_assigned_driver_id()
        0
        """
        return self.assigned_driver_id
    def get_request_wait_time(self):
        """This method is to get the information abut the requests current wait time.
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_wait_time()
        0
        """
        return self.wait_time
    def get_request_pickup_wait_time(self):
        """This method is to get the information abut the requests pickup_wait_time, and if this 
        has a value of 0 then that means that the request have not yet been picked up.
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_pickup_wait_time()
        0
        """
        return self.pickup_wait_time
    def get_request_delivered_wait_time(self):
        """This method is to get the information abut the requests delivered_wait_time, and if this 
        has a value of 0 then that means that the request have not yet been delivered.
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_delivered_wait_time()
        0
        """
        return self.delivered_wait_time
    def get_request_expired_wait_time(self):
        """This method is to get the information abut the requests expired_wait_time, and if this 
        has a value of 0 then that means that the request have not expired, and if the delivered_wait_time
        also have a value of 0 then the request is still active and if it will be delivered or will end
        expiring is to be determined.
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        >>> r.get_request_expired_wait_time()
        0
        """
        return self.expired_wait_time

    # Setters : there will be a setter for everey object in the request
    #def set_request():
         #"""This method is a placeholder for if it is nessesary to have a setter for the hwole request
         #"""

         # OBS!!!!!! I set skal den retunere self???? 
         
    def set_request_rid(self, rid: int):
        """"This method is to set the information in a request to a specefic request id
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 

        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_rid(5)
        >>> print(r)
        id: 5,
        pickup: 0, 0,
        dropoff: 20, 10,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 0
        
        """
        if self.is_one_valid("rid", rid):
             self.rid = rid
             return self
        else:
             raise ValueError("Invalid value for the id (=rid), it can not be a negative number and it have to be a integrear of 1 or more")
        
    def set_request_pickup(self, pickup: Point):
        """This method is to set the information in a request to a specefic request pickup point.
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(15, 15)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_pickup(pickupPoint)
        >>> print(r)
        id: 5,
        pickup: 15, 15,
        dropoff: 20, 10,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 0
        
        """
        if self.is_one_valid("pickup", pickup):
             self.pickup = pickup
             return self
        else:
             raise ValueError("Invalid value for the picup object. The value have to be of the Point class")
        
    def set_request_dropoff(self, dropoff: Point):
        """This method is to set the information in a request to a specefic request dropoff point.
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(15, 15)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(25, 15)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_dropoff(dropoffPoint)
        >>> print(r)
        id: 1,
        pickup: 15, 15,
        dropoff: 25, 15,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 0
        
        """
        if self.is_one_valid("dropoff", dropoff):
            self.dropoff = dropoff
            return self
        else:
            raise ValueError("Invalid value for the dropoff objedt. The value have to be of the Point class")
        
    def set_request_creation_time(self, creation_time: int):
        """This method is to set the information in a request to a specefic request creation_time.
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(15, 15)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(25, 15)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_creation_time(10)
        >>> print(r)
        id: 1,
        pickup: 15, 15,
        dropoff: 25, 15,
        creation_time: 10,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 0

        """
        if self.is_one_valid("creation_time", creation_time):
            self.creation_time = creation_time
            return self
        else:
            raise ValueError("Invalid value for creation_time object. The Value have to be an integer.")

    def set_request_status(self, status: str):
        """This method is to set the information in a request to a specefic request status
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(15, 15)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(25, 15)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_status("DELIVERED")
        >>> print(r)
        id: 1,
        pickup: 15, 15,
        dropoff: 25, 15,
        creation_time: 0,
        status: DELIVERED,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 0

        """
        if self.is_one_valid("status", status):
            self.status = status
            return self
        else:
            raise ValueError("Invalid value for status")
        
    def set_request_assigned_driver_id(self, assigned_driver_id: int):
        """This method is to set the information in a request to a specefic request status
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(15, 15)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(25, 15)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_assigned_driver_id(70)
        >>> print(r)
        id: 1,
        pickup: 15, 15,
        dropoff: 25, 15,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 70,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 0
        
        """
        if self.is_one_valid("assigned_driver_id", assigned_driver_id):
            self.assigned_driver_id = assigned_driver_id
            return self
        else:
            raise ValueError("Invalid value for assigned_driver_id")
        
    def set_request_wait_time(self, wait_time):
        """This method is to set the information in a request to a specefic request wait_time.
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(15, 15)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(25, 15)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_wait_time(40)
        >>> print(r)
        id: 1,
        pickup: 15, 15,
        dropoff: 25, 15,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 40, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 0
        
        """
        if self.is_one_valid("wait_time", wait_time):
            self.wait_time = wait_time
            return self
        else:
            raise ValueError("Invalid value for wait_time")

    def set_request_pickup_wait_time(self, pickup_wait_time):
        """This method is to set the information in a request to a specefic request pickup_wait_time.
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(15, 15)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(25, 15)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_pickup_wait_time(40)
        >>> print(r)
        id: 1,
        pickup: 15, 15,
        dropoff: 25, 15,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 40,
        delivered_wait_time: 0,
        expired_wait_time: 0

        """
        if self.is_one_valid("pickup_wait_time", pickup_wait_time):
            self.pickup_wait_time = pickup_wait_time
            return self
        else:
            raise ValueError("invalid value for pickup_wait_time")
        
    def set_request_delivered_wait_time(self, delivered_wait_time):
        """This method is to set the information in a request to a specefic request delivered_wait_time.
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(15, 15)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(25, 15)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_delivered_wait_time(40)
        >>> print(r)
        id: 1,
        pickup: 15, 15,
        dropoff: 25, 15,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 40,
        expired_wait_time: 0
        
        """
        if self.is_one_valid("delivered_wait_time", delivered_wait_time):
            self.delivered_wait_time = delivered_wait_time
            return self
        else:
            raise ValueError("invalid value for delivered_wait_time")
        
    def set_request_expired_wait_time(self, expired_wait_time):
        """This method is to set the information in a request to a specefic request expired_wait_time.
        First it will validate the value acording to the request specefic rules and if the value
        is acceptable then it will the request value will be changed. If not then there will be 
        rasied an error. 
        It uses the validation metod of is_one_valid(). 
        
        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(15, 15)
        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(25, 15)
 
        >>> r = request(
            rid = 1,
            pickup = pickupPoint,
            dropoff = dropoffPoint,
            creation_time = 0,
            status = "WAITING",
            assigned_driver_id = 0,
            wait_time = 0,
            pickup_wait_time = 0,
            delivered_wait_time = 0,
            expired_wait_time = 0
        )
        
        >>> r.set_request_expired_wait_time(40)
        >>> print(r)
        pickup: 15, 15,
        dropoff: 25, 15,
        creation_time: 0,
        status: WAITING,
        assigned_driver_id: 0,
        wait_time: 0, 
        pickup_wait_time: 0,
        delivered_wait_time: 0,
        expired_wait_time: 40
        
        """
        if self.is_one_valid("expired_wait_time", expired_wait_time):
            self.expired_wait_time = expired_wait_time
            return self
        else:
            raise ValueError("invalid value for expired_wait_time")

    @staticmethod
    def is_one_valid(name, value):
        """This method is to validate the atributes there are in __init__. This valueates the objects
        is acceptable for the type class. 
        This method have to regonice from the setter what object is to validated. The knowlage of 
        what is to validated comes from the setter metod itself. 

        If the validated object can be accepted it will return True and if the object can not be 
        accepted then it will return False. 

        >>> request.is_one_valid("rid", 3)
        True
        >>> request.is_one_valid("rid", 3.6)
        False

        >>> pickupPoint = Point()
        >>> pickupPoint.set_point(0, 0)
        >>> request.is_one_valid("pickup", pickupPoint)
        True
        >>> request.is_one_valid("pickup", 5)
        False

        >>> dropoffPoint = Point()
        >>> dropoffPoint.set_point(20, 10)
        >>> request.is_one_valid("dropoff", dropoffPoint)
        True
        >>> request.is_one_valid("dropoff", 5)
        False

        >>> request.is_one_valid("creation_time", 6)
        True
        >>> request.is_one_valid("creation_time", 8.8)
        False

        >>> request.is_one_valid("status", "WAITING")
        True
        >>> request.is_one_valid("status", "ASSIGNED")
        True
        >>> request.is_one_valid("status", "PICKED")
        True
        >>> request.is_one_valid("status", "DELIVERED")
        True
        >>> request.is_one_valid("status", "EXPIRED")
        True
        >>> request.is_one_valid("status", "Helo")
        False
        >>> request.is_one_valid("status", 5)
        False

        >>> request.is_one_valid("assigned_driver_id", 7)
        True

        >>> request.is_one_valid("wait_time", 55)
        True

        >>> request.is_one_valid("pickup_wait_time", 55)
        True

        >>> request.is_one_valid("delivered_wait_time", 55)
        True

        >>> request.is_one_valid("expired_wait_time", 55)
        True
        
        """
        if name == "rid":
            return isinstance(value, int) and value >= 0
        if name == "pickup":
            return isinstance(value, Point)
        if name == "dropoff":
            return isinstance(value, Point)
        if name == "creation_time":
            return isinstance(value, int) and value >= 0
        if name == "status":
            if value in ("WAITING", "ASSIGNED", "PICKED", "DELIVERED", "EXPIRED"):
                return True
            else:
                return False
        if name == "assigned_driver_id":
            return isinstance(value, int)
        if name == "wait_time":
            return isinstance(value, int) and value >= 0
        if name == "pickup_wait_time":
            return isinstance(value, int) and value >= 0
        if name == "delivered_wait_time":
            return isinstance(value, int) and value >= 0
        if name == "expired_wait_time":
            return isinstance(value, int) and value >= 0
        
        return False

#----------------------------------------------------------------------------#
#     Driver classes
#----------------------------------------------------------------------------#

class historyevent:
    """This dataclass are to define a history event structure that easy can be 
    reacted and added to a dictory in the driverclass so that the history for
    a driver can extend, expand and save all the events that the driver is 
    going though
    """
    def __init__(self, timestamp: int, event: str, request_id: int | None = None, earnings: float | None = None, behaviour: str) -> None:
        if self.is_valid(timestamp, event, request_id, earnings):
            self.timestamp = timestamp
            self.event = event
            self.request_id = request_id
            self.earnings = earnings
            self.behaviour = behaviour 
        else:
            raise ValueError("Invalid value for one of the historyevent attributes values.")

    @staticmethod
    def is_valid(timestamp, event, request_id, earnings):
        """This method is to validate the dataclass historyevent when it is 
        created
        """
        if not isinstance(timestamp, int) or timestamp < 0:
            return False
        if not isinstance(event, str):
            return False
        if request_id is not None and (not isinstance(request_id, int) or request_id < 0):
            return False
        if earnings is not None and (not isinstance(earnings, int) or earnings < 0):
            return False
        
        return True

    def __repr__(self) -> str:
        """This is a representation of the dataclass that enable it to be used
        in the driver class
        """
        return (
            f"historyevent(timestamp = {self.timestamp}, "
            f"event = '{self.event}', "
            f"request_id = {self.request_id}, "
            f"earnings = {self.earnings})"
        )
    
        
class driver:
    """Dockstring"""
    def __init__(self, did: int, position: Point, speed: float, status: str, current_request: request | None, behaviour: DriverBehaviour):
        if self.is_valid(did, position, speed, status, current_request):
            self.did = did
            self.position = position
            self.speed = speed
            self.status = status
            self.current_request = current_request
            self.behaviour = behaviour
            self.history : list[historyevent] = []
            self.total_earnings = 0
            self.idle_time = 0
            self.idle_stattime = 0
            self.behaviour_mutation_stamp: int = 0
        else:
            raise ValueError("invalid valie for one of the driver attributes values")
    
    @staticmethod
    def is_valid(did, position, speed, status, behaviour, current_request):
        """This is to validate the objects in the class of driver. 
        It validate all but two of the objects. The objects not to be validated
        though this is the history and the behaviour and that becouse they are validated
        in other calsses. 
        """
        if not isinstance(did, int) or did < 0:
            return False
        if not isinstance(position, Point):
            return False
        if status not in ("IDLE", "TO_PICKUP", "TO_DROPOFF"):
            return False
        if behaviour not in (greedydistancebehaviour, earningsmaxbehaviour, lazybehaviour, naive):
            return False
        if current_request is not None and not isinstance(current_request, request):
            return False
        if not isinstance(speed, (int, float)) or speed < 0:
            return False
        
        return True

    # log_event used in dirver class -> also takes info from request
    def log_event(self, timestamp: int, event: str, request_id = None, earnings = None, behaviour):
        """This method is to be able to log events into the history 
        
        OBS: Jeg ved ikke hvor beregningen for vores earnings skal stå og hvad den 
        bliver kaldt men den skal arbejde sammen med denne del. 
        """
        self.history.append(historyevent(timestamp, event, behaviour, request_id, earnings))    

    # help for mutation rule classes
    def all_events_since_last_mutation(self):
        return [ev for ev in self.history if ev.timestamp >= self.behaviour_mutation_stamp]
    
    # help for mutation rule classes
    def update_behaviour_and_stamp(self, new_time, new_behavior):
        """This method is so that mutation rule can easyly change stats for the
        drivers behavior and that the behaviour_mutation_stamp it set to current 
        time"""
        self.behaviour_mutation_stamp = new_time
        self.behaviour = new_behavior
        return

    # help for mutation rule classes
    #def get_whole_driver_history

    # help for mutation rule classes
    #def 
    
    def decide(self, offer: offer, time: tick) -> bool:
        return self.behaviour.decide(self, offer, time)

    
    def assign_request(self, offer: offer, current_time: int) -> None:
        """Thus method is to assign a request to a driver. This will also work
        with the request class and its methods.

        The first thing is to check if the driver aldredy are on a job. So if
        the driver do not have the status of "IDLE" then the driver is alredy
        on a job and should not be taking on another job. 

        Then it have to look at the request that the driver want to accept. If
        this request have the status "WAITING" then the driver can accept the
        request. If the request have any else status, then the request is 
        appointed to another driver and is not a request that the driver can 
        take. 

        Then the driver have to look at its own behaveour and if the drivers
        behaviour allign with acceptning the request then the driver will accept
        the request and status'es for the driver and the request will be changed.

        First of all this method will first check that the request status is 
        "WAITING", else then the driver should not take the request. 
        """
        if self.status != "IDLE":
            return
        if request.status == "WAITING":
            if self.decide(self, offer, current_time): # MANGLER ########################
                offer.request.mark_assigned(self.did)
                self.current_request = offer.request
                self.status = "TO_PICKUP"
                self.log_event(current_time, "ASSIGNED", offer.request.rid)
                self.idle_time = 0
                self.idle_stattime = 0
            else: # ved ikke om det er here den skal decline??? 
                self.idle_time = current_time - self.idle_stattime
            #self.idle_since = current_time

    def target_point(self) -> Optional[Point]:
        """This method makes the driver class able to obtain a target point
        from the current request of the driver whit the working os the 
        request class mehtods
        """
        if self.current_request is None:
            return None # er ikke sikker på om denne skal være der eller det efter "and"
        if self.status == "TO_PICKUP" and self.current_request:
            return self.current_request.pickup
        if self.status == "TO_DROPOFF" and self.current_request:
            return self.current_request.dropoff
        return None

    def step(self, tick: int) -> None:
        """Moves the driver towards the current target according to speed and 
        the time step dt.
        
        OBS!!! Hvad har laust kaldt tiden der går? har han kaldt opdateringen
        pr. time update/ step dt???? 
        dt = "delta time" the time step that passes between each update of
        the system???? 

        The update current time will be updated with??? 
        mabey : current_time += dt

        Først finder den target ud fra den request som den lige nu har aktiv. 
        Hvis der ingen target er lige nu sker der ingnenting. 
        Hvis der dog er et target så vil driver bestemmer den distancen 
        mellem sig selv og target. Derefter skal driver også bestemme hvor
        langt at denne driver kan bevæge sig pr tidsenhed som er drivers 
        speed * tidsenhed, som kaldes max_move. Hvis dette max_move er lig 
        med eller mindre end den distance der er mellem driver og target så
        vil drivers position blive til target positionen. Hvis det max som 
        driver kan køre er mindre en den distance til target så skal driver 
        bevæge sig sit max imod target og derfor skal have en ny position. 
        
        The samll part part/distance that the driver will move is a part of 
        the vector between the driver position and the target is a segment of
        the full vector. Now the direction of the vector found and it is 
        normalized by using the distance. Then using the normalized direction 
        with the max_move is used to calculate the new postition. 
        Driver position : (X, Y)
        target postiion : (Xt, Yt)
        Max_move : speed * timeelement
        Direction vector : ((dx = Xt - X), (dy = Yt - Y))
        Distance : sqrt((dx) ** 2 + (dy) ** 2)
        Normalize direction : Nx = dx / distance  and  Ny = dy / distance
        New position : ((x' = X + Nx * max_move), (y' = Y + Ny * max_move))

        Math about vectors read from: book : hardcore programming for mechanical engineers        
        """
        target = self.target_point()
        if target is None:
            return
        
        max_move = self.speed * tick  # maxx move driver -> the driver movment pr. timeelement
        dx = target.x - self.position.x # Direction vector x coordinat
        dy = target.y - self.position.y # Direction vector y coordinat

        dist_from_driver_to_target = self.position.distance_to(target)

        if dist_from_driver_to_target <= max_move:
            self.position = Point(target.x, target.y)
            return 
        else:
            Nx = dx / dist_from_driver_to_target # Normalize direction vevtor x coordinat
            Ny = dy / dist_from_driver_to_target # Normalize direction vevtor y coordinat
            new_x_pos = self.position.x + (Nx * max_move) # New driver position x coordinate 
            new_y_pos = self.position.y + (Ny * max_move) # New driver position y coordinate 
            self.position = Point(new_x_pos, new_y_pos)

    def complete_pickup(self, time: int) -> None:
        """Updates internal state when the pickup is reached.
        
        But first it have to check that the current request is not none (that the driver
        have a request) and that the driver status is current in "TO_PICKUP" status and 
        lastly the last check is that the driver position is indeed at the pickup position. 
        Instad of using the '==' or '=' to check if the driver is at the position of the
        pickup the isclose function are utilized. By default it have a tolerance of 
        1e-09 = 0.0000000010 differnce. This is becouse when comparing two floats that is
        changing in a simulation (or in most code where the float is used) the rounding
        of the decimal can make the number vary a little bit with a wery small decimal. 
        This can mean that even if the driver have come to the place for the pickup if 
        i validate it with testing if the two positions are equal to each other then 
        when mooving if the position of one is just a tiny bit of  and not EXCATY then
        it can return falsly False. 
        So instad it is validated with iscloase() method from the python standard 
        library. There is also an equal method named isclose() in the module of 
        numpy. 
        """
        if self.current_request is None:
            return None
        if self.status == "TO_PICKUP":
            if math.isclose(self.position.x, self.current_request.pickup.x) and math.isclose(self.position.y, self.current_request.pickup.y):
                self.current_request.mark_picked(time)
                self.status = "TO_DROPOFF"
                self.log_event(time, "PICKED", self.behaviour, self.current_request.rid)


    def complete_dropoff(self, time: int) -> None: # ,earning
        """Updates internal state and history when the drop-oﬀ is reached.
        
        OBS!: hvis der skal være i driver history hvad driver ahr tjent så skal dette 
        også gives her: 
        """
        if self.current_request is None:
            return None
        if self.status == "TO_DROPOFF":
            if math.isclose(self.position.x, self.current_request.dropoff.x) and math.isclose(self.position.y, self.current_request.dropoff.y):
                self.current_request.mark_delivered(time)
                self.log_event(time, "DELIVERED", self.behaviour, self.current_request.rid) # ,earning
                #self.total_earnings += earning
                self.current_request = None
                self.status = "IDLE"
                self.idle_stattime = time


    def __str__(self):
        """This method is specefi how the code will reprecent the class object as an string."""
        return f"did = {self.did},\n position = {self.position},\n status = {self.status},\n current_request = {self.current_request},\n behaviour = {self.behaviour},\n history = {self.history},\n total_earnings = {self.total_earnings},\n idle_time = {self.idle_time},\n idle_stattime = {self.idle_stattime}"


    def __repr__(self):
        """This method are to return a representation of a request, so the returned is 
        numerica and can be used in other methods sofouth.
        
        """
        return f"driver(did = {self.did}, position = {self.position}, speed = {self.speed}, status = {self.status}, current_request = {self.current_request}, history = {self.history}, total_earnings = {self.total_earnings}, idle_time = {self.idle_time}, idle_stattime = {self.idle_stattime})"

    def copy_driver(self):
        return driver(self.did(), 
                      self.position(), 
                      self.speed(), 
                      self.status(), 
                      self.current_request(), 
                      self.behaviour(),
                      self.history(),
                      self.total_earnings(),
                      self.idle_time(),
                      self.idle_stattime())

    def update_totalearnings(self, earning: int):
        """This method
        
        OBS: Hvor skal der stå det med distance i forhold til hvis der sker
        en delivery? -> se også: "complete_dropoff" fordi der kan totalearnings også 
        blive opdateret igennem. Denne skal bruges hvis det skal være noget simulationen
        gør.
        """
        self.total_earnings += earning

    # Getters
    ## placeholder for the get it all if nessesary but there is alredy repr, str and copy

    def get_driver_id(self):
        """This method is to be able to get the information driver id (did) from the
        driver.
        """
        return self.did
    
    def get_driver_position(self):
        """This method is to be able to get the information driver position from driver.
        """
        return self.position

    def get_driver_speed(self):
        """This method is to be able to get the information driver speed from driver.
        """
        return self.speed

    def get_driver_current_request(self):
        """This method is to be able to get the information driver currrent_request 
        id (rid) from driver. Then if the entire request is needed or all the 
        information can be found though the knowlage of the request id.
        """
        return self.current_request.rid
    
    def get_driver_behaviour(self):
        """This method is to be able to get the information about witch 
        driver behaviour this driver displays. 

        OBS: Jeg skal finde ud af om driverbeheveoir skal have et navn og det er 
        den inforamtion som den giver tilbage eller om den skal give alt informationen
        eller noget andet.
        """
        return self.behaviour
    #OBS skal lige tjekke om denne passer

    def get_driver_history(self):
        """This method is to be able to get the information driver history
        """
        return self.history

    
    # Setteres
    @staticmethod
    def is_one_valid(name, value):
        """This method is to able to validate the induvidual infomation that is to be
        changed though set.
        Some of the values / objects of the driver information can not be set in the 
        way of set method therefore there is not a induvidual validation. 
        """
        if name == "did":
            return isinstance(value, int) and value >= 0
        if name == "position":
            return isinstance(value, Point)
        if name == "speed":
            return isinstance(value, (int, float))
        if name == "status":
            if value in ("IDLE", "TO_PICKUP", "TO_DROPOFF"):
                return True
            else:
                return False
        return False


    def set_driver_id(self, did: int):
        """This method is to set the information of driver id (did) to something given.
        """
        if self.is_one_valid("did", did):
            self.did = did
            return self
        else:
            raise ValueError("invalid value for the did you wanted to give a driver")
    
    def set_driver_position(self, position: Point):
        """This method is to set the driver to a another specefic postiion.
        """
        if self.is_one_valid("position", position):
            self.position = position
            return self
        else:
            raise ValueError("invalid value for the driver position you wanted to give the driver")

    def set_driver_speed(self, speed: float):
        """This method is to change the speed of a driver to given speed.
        """
        if self.is_one_valid("speed", speed):
            self.speed = speed
            return self
        else:
            raise ValueError("invalid value for the speed that you wanted to give to a driver")

#----------------------------------------------------------------------------#
#     Driver behaviour classes
#----------------------------------------------------------------------------#
class driverbehaviour(ABC):
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
    def decide(self, driver: driver, offer: offer, time: int) -> bool:
        """This will return True if the driver accepts the offer of the request, Flase
        otherwise.
        254
        State pattern
        """
        raise NotImplementedError

class greedydistancebehaviour(driverbehaviour):
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
    def __init__(self, max_distance: float = 0.0, expiretime: int):
        self.max_distance = max_distance
        self.expiretime = expiretime

    def decide(self, driver: driver, offer: offer, timer: tick) -> bool:
        if self.max_distance == 0:
            self.max_distance = (driver.speed * self.expiretime)
        max_distance_to_pickup = self.max_distance / 3
        pick_dist = driver.position.distance_to(offer.request.pickup)
        if pick_dist <= max_distance_to_pickup and offer.request.dropoff < self.max_distance:
            return True
        else: 
            False

class earningsmaxbehaviour(driverbehaviour):
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
        
    def decide(self, driver: driver, offer: offer, timer: tick) -> bool:
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


class lazybehaviour(driverbehaviour):
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

    def decide(self, driver: driver, offer: offer, timer: tick) -> bool:
        """This is the part that evaluate if the request offer allign with the
        behavior of the driver
        """
        idle_time = driver.idle_time
        distance_to_pickup = driver.position.distance_to(offer.request.pickup)
        if distance_to_pickup <= self.close and idle_time >= self.max_idle_time:
            return True
        else:
            return False
        

class naive(driverbehaviour):
    """This behavior accepts ALL!"""
    def decide(self, driver, offer, time):
        return True


#----------------------------------------------------------------------------#
#     Mutate classes
#----------------------------------------------------------------------------#

# Driver → History → MutationManager → Rules

class mutationsthresholds:
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

class mutationrule(ABC):
    """This is the parent class / base class to all the mutations rules.

    """
    def maybe_mutate(self, driver: driver, time: int) -> None:
        """Return true if the driver should mutate / will mutate and False
        otherwise. Right now there is only one rule"""
        raise NotImplementedError
    
class desisionthreerule(mutationrule):
    """This mutation rule will follow a disision three. 
    
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
    def __init__(self, thresholds: mutationsthresholds) -> None:
        self.thresholds = thresholds

    @staticmethod
    def _random_behaviour():
        return random.choice([
            greedydistancebehaviour,
            earningsmaxbehaviour,
            lazybehaviour,
            naive
        ])

    def maybe_mutate(self, driver: driver, time: int) -> None:
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
        earnings_ratio = (sum(ev.earnings for ev in events if ev.event == "DELIVERED")) / time_since_last
        accepted_ratio = (sum(1 for ev in events if ev.event == "accepted")) / time_since_last

        # ------- check threshold ------------
        A = expired >= self.thresholds.expire_thr
        B = earnings_ratio < self.thresholds.earning_thr
        C = accepted_ratio < self.thresholds.accepted_thr

        if not (A or B or C):
            return  # if not threshold is reached then nothing happens

        # ------- mutation based on on reasent history ------------
        current_behaviour = driver.behaviour
        GreedyBe = greedydistancebehaviour
        EarningBe = earningsmaxbehaviour
        LasyBe = lazybehaviour
        NaiveBe = naive

        if A and not B and not C:
            driver.behaviour = GreedyBe if current_behaviour != GreedyBe else LasyBe

        elif B and not A and not C:
            driver.behaviour = EarningBe if current_behaviour != EarningBe else GreedyBe
        
        elif C and not A and not B:
            driver.behaviour = NaiveBe if current_behaviour != NaiveBe else EarningBe

        elif A and B and not C:
            driver.behaviour = GreedyBe if current_behaviour != GreedyBe else self._random_behaviour()

        elif B and C and not A:
            driver.behaviour = EarningBe if current_behaviour != EarningBe else NaiveBe

        elif A and C and not B:
            driver.behaviour = LasyBe if current_behaviour != LasyBe else self._random_behaviour()

        elif A and B and C:
            driver.behaviour = self._random_behaviour()

        # ------- Update mutation timestamp on driver ------------
        driver.behaviour_mutation_stamp = time

#----------------------------------------------------------------------------#
#     Generate classes
#----------------------------------------------------------------------------#

# OBS: at den skaber flere request efterhåneden som tiden går skal gøres pr tidsstep
# OBS jeg er ikke helt sikker på load delen på begge
class requestgenerator:
    """This class has to able to genereate requests pr. timestamp. 
    """
    def __init__(self, width: int =  50.0, height: int = 30.0):
        self.width = width
        self.height = height
        self._next_rid = 1

    def req_generate(self, time: int, req_rate: float):
        requests = []
        count = numpy.random.poisson(req_rate)
        time = time

        for _ in range(count):
            this_rid = self._next_rid
            self._next_rid += 1

            pickuppoint = Point(
                random.uniform(0, self.width),
                random.uniform(0, self.height)
            )
            dropoffpoint = Point(
                random.uniform(0, self.width),
                random.uniform(0, self.height)
            )

            req = request(
                rid = this_rid,
                pickup = pickuppoint,
                dropoff = dropoffpoint,
                creation_time=time
            )

            requests.append(req)
        return requests
    
    def load_from_cvs(self, path: str):
        requests = []
        with open(path) as csvfil:
        for line in csvfil:
            if "-" in line:
                raise ValueError("Error : there is a negative value in the csv file. None of the given information can have a negative value.")
                #print("Error : there is a negative value in the csv file. None of the given information can have a negative value.")
                # system exit
        full_clean_file = []
        with open(path, "r") as cvsfil:
            next(cvsfil) # skip header
            for row in cvsfil:
                clean = [p.strip() for p in row.split(",")]
                clean_float = []
                for i in clean:
                    if i.isdigit():
                        clean_float.append(float(i))
                full_clean_file.append(clean_float)
        
        # Check that the seperator in the file is indeed ",".
        with open(path, "r") as csvfile:
            for row in csvfile:
                # Validate that the file content, that the file information is seperated by ",".
                seperators = [";", " ", "\t", ",", ":"] # IF time make the test for others seperators work
                
                counts = {d: row.count(d) for d in seperators}
                if counts[","] > 0:
                    continue
                else:
                    raise ValueError("Error: Inconsistent separator found in file. You may have used the wrong file.")
                    # print("Error: Inconsistent separator found in file. You may have used the wrong file.")
                    "system stop"

        # Check the csv file for that the right amount of information is precent in each row and that the coordiantes match that of the grid.
        count_id_gridchek = 1 # request ID counter
        for row in full_clean_file:
            no_info_row = len(row)
            if not no_info_row == 5 or no_info_row == 6: # Check how many values are in the row after conversion. There should be 5 or 6 values. Be aware that negative numbers will diapear and therefore trigger this check but any negative numbers should be found in previous checks.
                raise ValueError(f"Error : Csv file rows have the incorrect number of values. Each row must contain either 5 or 6 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include, the error occured in row no. {count_id_gridchek}.")
                    # print(f"Error : Csv file rows have the incorrect number of values. Each row must contain either 5 or 6 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include, the error occured in row no. {count_id_gridchek}.")
                    # system stop or call the function again
            if not (row[1] <= 50.0) and (row[3] <=50.0): # Chek tht the x coordinates (witch) from the file is not highter than the defould grid width (50.0)
                raise ValueError(f"Error : An x coordinates that cooresponds to the placement in the grid width are highter than the max width. The error is to be found in the columns of x picup and/or x delivery. The error occured in row no. {count_id_gridchek}.")
                #print(f"Error : An x coordinates that cooresponds to the placement in the grid width are highter than the max width. The error is to be found in the columns of x picup and/or x delivery. The error occured in row no. {count_id_gridchek}.") 
                # system stop
            if not (row[2] <=30.0) and (row[4] <= 30.0): # Chek tht the y coordinates (hight) from the file is not highter than the defould grid hight (30.0)
                raise ValueError(f"Error : An y coordinate that coorespond to the placement in the grid hight are higher than the max hight. The error is to be found in the columns of y picup and/or y delivery. The error occured in row no. {count_id_gridchek}.")
                # print(f"Error : An y coordinate that coorespond to the placement in the grid hight are higher than the max hight. The error is to be found in the columns of y picup and/or y delivery. The error occured in row no. {count_id_gridchek}.")
            count_id_gridchek += 1
        
        # Chek that the column of the request time is indeed in an increasing value order. Becouse you can not place orders in the past.
        last_request_time = 0 # The last request time placeholder to compare to ensure that the request_time information is in a increasing order.
        for row in full_clean_file:
            if not (row[0] >= last_request_time):
                raise ValueError("The request time (forst column) in the csv file is not in a increasing value order. Please correct the error before trying again")
                # print("The request time (forst column) in the csv file is not in a increasing value order. Please correct the error before trying again")
                # system stop
            else:
                last_request_time = row[0]

        # Make the request list[dict] that is needed for the simulation
        requests = []
        time = time 
        for row in full_clean_file:
            pickuppoint = Point(row[1], row[2])
            dropoffpoint = Point(row[3], row[4])
            r = request(
                rid = self._next_rid,
                pickup = pickuppoint,
                dropoff = dropoffpoint,
                creation_time = time,
            )
            self._next_rid += 1
            requests.append(r)
        return requests



class drivergenerator:
    """This class has to be able to generate drivers as a one time thing but also
    be able to read a cvs file and use those drivers"""
    def __init__(self, width: float = 50.0, height: float = 30.0):
        self.width = width
        self.height = height
        self._next_did = 1

    @staticmethod
    def _random_behaviour():
        return random.choice([
            greedydistancebehaviour,
            earningsmaxbehaviour,
            lazybehaviour,
            naive
        ])

    def generate(self, n: int):
        drivers = []

        for did in range(n):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            speed = random.uniform(0.5, 3.0)
            #behav = [greedydistancebehaviour, earningsmaxbehaviour, lazybehaviour, naive]
            #sbehav = random.choice(behav)
            behavv = self._random_behaviour()

            driver = driver(
                did = did,
                position = Point(x, y),
                speed = speed.
                behaviour = behavv,
            )

            drivers.append(driver)
        return drivers
    
    def load_from_cvs(self, path: str):
        drivers = []
        with open(path) as csvfil:
            for row in csvfil:
                # Validate the file content, is the file seperated by ",".
                seperators = [";", " ", "\t", ",", ":"]
                counts = {d: row.count(d) for d in seperators}
                if counts[","] > 0:
                    continue
                else:
                    raise ValueError("Error: Inconsistent separator found in file. You may have used the wrong file."))
                    #print("Error: Inconsistent separator found in file. You may have used the wrong file.")
                    #"""system stop"""
        with open(path) as csvfil:
            for line in csvfil:
                if "-" in line:
                    raise ValueError("Error : there is a negative value in the csv file. None of the given information can have a negative value.")
                    #print("Error : there is a negative value in the csv file. None of the given information can have a negative value.")
                    # system exit
        with open(path, "r") as cvsfil:
            next(cvsfil) # skip header
            for row in cvsfil:
                clean = [p.strip() for p in row.split(",")] # Remove any leading/trailing whitespace or newline characters

                # Convert the string values into float values if they are digits. 
                parts_float  = [] # List to hold the converted float values from the row
                for i in clean: # Convert each part to float if it is a digit
                    if i.isdigit():
                        parts_float.append(float(i))

                # Validate the number of values in each row after conversion to float. There should eighter be 2 or 3 values. 
                no_info_row = len(parts_float) # Count the number of values in the row after conversion to float.
                if not no_info_row == 2 or no_info_row == 3: # Check how many values are in the row after conversion. There should be 2 or 3 values. 
                    raise ValueError("Error : Csv file rows have the incorrect number of values. Each row must contain either 2 or 3 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include.")
                    # print("Error : Csv file rows have the incorrect number of values. Each row must contain either 2 or 3 values corresponding to x coordinat, y coordinat, and optional speed where speed is optional to include.")
                    # """sys.exit(1)""" # Exit the program if the row does not have the correct number of values.
                
                # Check if the coordiantes are within the grid bounds.
                x = parts_float[0]
                y = parts_float[1]
                if not (0 <= x <= 50.0) or not (0 <= y <= 30.0):
                    raise ValueError("Error : Coordinates for drivers are out of grid bounds.")
                    # print("Error : Coordinates for drivers are out of grid bounds.")
                    # """system stop"""

                 # Create the driver dictionary
                if no_info_row == 3:
                    the_speed = parts_float[2] # If speed is provided then use it.
                else:
                    the_speed = random.uniform(0.5, 3.0) # If speed is not provided use a random speed between 0.5 and 3.0
                    d = driver(
                        did = self._next_did,
                        position = Point(x, y),
                        speed = the_speed
                    )
                self._next_did += 1
                drivers.append(d)
        return drivers

 