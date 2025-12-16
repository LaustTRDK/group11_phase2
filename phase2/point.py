from __future__ import annotations
import math

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