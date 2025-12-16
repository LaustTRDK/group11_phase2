from __future__ import annotations
from .point import Point
from .request import Request
import random
import numpy

class RequestGenerator:
    """This class has to able to genereate requests pr. timestamp. 
    """
    def __init__(self, rate: float, width: float = 50.0, height: float = 30.0, next_id: int = 1, scheduled: list = None):
        self.rate = rate
        self.width = width
        self.height = height
        self._next_rid = next_id
        self.scheduled = scheduled or []

    def maybe_generate(self, time: int) -> list[Request]:
        # Find and return scheduled requests that match current time
        result = [r for r in self.scheduled if r.creation_time == time]
        
        # Remove returned requests from scheduled list
        self.scheduled = [r for r in self.scheduled if r.creation_time != time]
        
        # Add newly generated random requests
        result.extend(self.req_generate(time, self.rate))
        
        return result

    def req_generate(self, time: int, req_rate: float) -> list[Request]:
        requests = []
        count = numpy.random.poisson(req_rate)
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

            req = Request(
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
            r = Request(
                rid = self._next_rid,
                pickup = pickuppoint,
                dropoff = dropoffpoint,
                creation_time = time,
            )
            self._next_rid += 1
            requests.append(r)
        return requests




class DriverGenerator:
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
                speed = speed,
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
                    raise ValueError("Error: Inconsistent separator found in file. You may have used the wrong file.")
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