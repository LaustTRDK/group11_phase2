from __future__ import annotations
import math
from typing import Optional

from .driver_behaviour import DriverBehaviour
from .request import Request
from .point import Point
from .offer import Offer

class HistoryEvent:
    """This dataclass are to define a history event structure that easy can be 
    reacted and added to a dictory in the driverclass so that the history for
    a driver can extend, expand and save all the events that the driver is 
    going though
    """
    def __init__(self, timestamp: int, event: str, behaviour: str, request_id: int | None = None, earnings: float | None = None) -> None:
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
    
        
class Driver:
    """Dockstring"""
    def __init__(self, did: int, position: Point, speed: float, status: str, current_request: Request | None, behaviour: DriverBehaviour):
        if self.is_valid(did, position, speed, status, behaviour, current_request):
            self.did = did
            self.position = position
            self.speed = speed
            self.status = status
            self.current_request = current_request
            self.behaviour = behaviour
            self.history : list[HistoryEvent] = []
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
        if behaviour is not None and not isinstance(behaviour, DriverBehaviour):
            return False
        if current_request is not None and not isinstance(current_request, Request):
            return False
        if not isinstance(speed, (int, float)) or speed < 0:
            return False
        
        return True


    # log_event used in dirver class -> also takes info from request
    def log_event(self, timestamp: int, event: str, behaviour, request_id=None, earnings=None):
        """This method is to be able to log events into the history 
        
        OBS: Jeg ved ikke hvor beregningen for vores earnings skal stå og hvad den 
        bliver kaldt men den skal arbejde sammen med denne del.
        """
        self.history.append(HistoryEvent(timestamp, event, behaviour, request_id, earnings))    

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
    
    def decide(self, offer: Offer, time: int) -> bool:
        return self.behaviour.decide(self, offer, time)

    
    def assign_request(self, request: Request, current_time: int) -> None:
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
            # Create an Offer object for the behaviour.decide method
            offer = Offer(self, request, 0.0, 0.0)
            if self.behaviour.decide(self, offer, current_time):
                request.mark_assigned(self.did)
                self.current_request = request
                self.status = "TO_PICKUP"
                self.log_event(current_time, "ASSIGNED", request.rid)
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