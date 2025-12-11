import numpy, os, decorator, math
# from matplotlib import 
from dataclasses import dataclass
from __future__ import annotations
from typing import Any, List, Optional, Tuple
from collections import deque

# Core Domain Classes
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
        """What is this method used for. 
        what can the objects be ant not be.
        docktest.
        potential value errors. 
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
        if not isinstance(rid, int) and rid < 0:
            return False
        if not isinstance(pickup, Point):
            return False
        if not isinstance(dropoff, Point):
            return False
        if not isinstance(creation_time, int) and creation_time < 0:
            return False
        if status not in ("WAITING", "ASSIGNED", "PICKED", "DELIVERED", "EXPIRED"):
            return False
        if assigned_driver_id is not None and not isinstance(assigned_driver_id, int) and assigned_driver_id < 0:
            return False
        if not isinstance(wait_time, int) and wait_time < 0:
            return False
        if not isinstance(pickup_wait_time, int) and pickup_wait_time < 0:
            return False
        if not isinstance(delivered_wait_time, int) and delivered_wait_time < 0:
            return False
        if not isinstance(expired_wait_time, int) and expired_wait_time < 0:
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
        self.wait_time = current_time
    
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
        return request(self.rid(), self.pickup(), self.dropoff(), self.creation_time(), self.wait_time(), self.assigned_driver_id(), self.wait_time())
    
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

