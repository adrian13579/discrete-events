from .random_variables import generate_client, normal, poisson, exponential
from collections import deque


class HappyComputing:
    """
    This class represent the simulation of Happy Computing repair shop.
    In this simulation there are 2 sellers, 3 technicians and 1 specialized
    technician.
    """

    def __init__(self, T: int = 480):
        self.cost = {1: 0, 2: 350, 3: 500, 4: 750}

        # Time variables
        self.T = T
        self.time = 0

        self.time_arrival = 0
        self.time_departure_seller_1 = float("inf")
        self.time_departure_seller_2 = float("inf")
        self.time_departure_technician_1 = float("inf")
        self.time_departure_technician_2 = float("inf")
        self.time_departure_technician_3 = float("inf")
        self.time_departure_specialized_technician = float("inf")

        # Counter variables
        self.arrivals_count = 0
        self.departure_count = 0
        self.arrival = {} 
        self.departure= {}  

        # State variables
        self.profits = 0

        # the following variables give the current type of client that is being attended.
        self.seller_1 = 0
        self.seller_2 = 0
        self.technician_1 = 0
        self.technician_2 = 0
        self.technician_3 = 0
        self.specialized_technician = 0

        self.sellers_queue = deque()
        self.technicians_queue = deque()

        self.n = 0 


    def state(self):
        return min(
            self.time_arrival,
            self.time_departure_seller_1,
            self.time_departure_seller_2,
            self.time_departure_technician_1,
            self.time_departure_technician_2,
            self.time_departure_technician_3,
            self.time_departure_specialized_technician,
        )

    def time_advance(self):
        """Move timeline to next event(s)"""

        if self.time_arrival > self.T:
            self.time_arrival = float('inf')

        if self.state() == self.time_arrival and self.time_arrival <= self.T:

            self.time = self.time_arrival
            self.time_arrival = self.time + poisson(20) 
            self.arrivals_count+= 1
            self.arrival[self.arrivals_count] = self.time
            self.sellers_queue.append(generate_client())
            self.n+=1

            if not self.seller_1 and self.sellers_queue:
                self.seller_1 = self.sellers_queue.popleft()
                self.time_departure_seller_1 = self.time + normal(5,2) 
            if not self.seller_2 and self.sellers_queue:
                self.seller_2 = self.sellers_queue.popleft()
                self.time_departure_seller_2 = self.time + normal(5,2)

        if self.state() == self.time_departure_seller_1 and (
            self.time_departure_seller_1 <= self.T or self.n > 0
        ):

            self.time = self.time_departure_seller_1

            client = self.seller_1
            if client == 4:
                self.profits += 750
                self.departure_count+=1
                self.departure[self.departure_count] = self.time
                self.n-=1
            else:
                self.technicians_queue.append(client)
                if not self.technician_1 and self.technicians_queue:
                    self.technician_1 = self.technicians_queue.popleft()
                    self.time_departure_technician_1 = self.time + exponential(1/20) 
                if not self.technician_2 and self.technicians_queue:
                    self.technician_2 = self.technicians_queue.popleft()
                    self.time_departure_technician_2 = self.time + exponential(1/20)
                if not self.technician_3 and self.technicians_queue:
                    self.technician_3 = self.technicians_queue.popleft()
                    self.time_departure_technician_3 = self.time + exponential(1/20)
                
                
                if not self.specialized_technician and self.technicians_queue:
                    try:
                        self.technicians_queue.remove(3)
                        self.specialized_technician = 3
                    except ValueError:
                        self.specialized_technician = self.technicians_queue.popleft()
                    self.time_departure_specialized_technician = self.time + exponential(1/15)

            if self.sellers_queue:
                self.seller_1 = self.sellers_queue.popleft()
                self.time_departure_seller_1 = self.time + normal(5,2) 
            else:
                self.seller_1 = 0
                self.time_departure_seller_1 = float("inf")

        if self.state() == self.time_departure_seller_2 and (
            self.time_departure_seller_2 <= self.T or self.n > 0
        ):

            self.time = self.time_departure_seller_2

            client = self.seller_2
            if client == 4:
                self.profits += 750
                self.departure_count+=1
                self.departure[self.departure_count] = self.time
                self.n-=1
            else:
                self.technicians_queue.append(client)
                if not self.technician_1 and self.technicians_queue:
                    self.technician_1 = self.technicians_queue.popleft()
                    self.time_departure_technician_1 = self.time + exponential(1/20)
                if not self.technician_2 and self.technicians_queue:
                    self.technician_2 = self.technicians_queue.popleft()
                    self.time_departure_technician_2 = self.time + exponential(1/20)
                if not self.technician_3 and self.technicians_queue:
                    self.technician_3 = self.technicians_queue.popleft()
                    self.time_departure_technician_3 = self.time + exponential(1/20)

                if not self.specialized_technician and self.technicians_queue:
                    try:
                        self.technicians_queue.remove(3)
                        self.specialized_technician = 3
                    except ValueError:
                        self.specialized_technician = self.technicians_queue.popleft()
                    self.time_departure_specialized_technician = self.time + exponential(1/15)

            if self.sellers_queue:
                self.seller_2 = self.sellers_queue.popleft()
                self.time_departure_seller_2 = self.time + normal(5,2)
            else:
                self.seller_2 = 0
                self.time_departure_seller_2 = float("inf")

        if self.state() == self.time_departure_technician_1 and (
            self.time_departure_technician_1 <= self.T
            or self.n > 0
        ):

            self.time = self.state()

            client = self.technician_1
            self.profits += self.cost[client]
            self.departure_count+=1
            self.departure[self.departure_count] = self.time
            self.n-=1

            if self.technicians_queue:
                self.technician_1 = self.technicians_queue.popleft()
                self.time_departure_technician_1 = self.time + exponential(1/20)
            else:
                self.technician_1 = 0
                self.time_departure_technician_1 = float("inf")

        if self.state() == self.time_departure_technician_2 and (
            self.time_departure_technician_2 <= self.T
            or self.n > 0
        ):

            self.time = self.state()

            client = self.technician_2
            self.profits += self.cost[client]
            self.departure_count+=1
            self.departure[self.departure_count] = self.time
            self.n-=1

            if self.technicians_queue:
                self.technician_2 = self.technicians_queue.popleft()
                self.time_departure_technician_2 = self.time + exponential(1/20)
            else:
                self.technician_2 = 0
                self.time_departure_technician_2 = float("inf")

        if self.state() == self.time_departure_technician_3 and (
            self.time_departure_technician_3 <= self.T
            or self.n > 0
        ):

            self.time = self.state()

            client = self.technician_3
            self.profits += self.cost[client]
            self.departure_count+=1
            self.departure[self.departure_count] = self.time
            self.n-=1

            if self.technicians_queue:
                self.technician_3 = self.technicians_queue.popleft()
                self.time_departure_technician_3 = self.time + exponential(1/20)
            else:
                self.technician_3 = 0
                self.time_departure_technician_3 = float("inf")

        if self.state() == self.time_departure_specialized_technician and (
            self.time_departure_specialized_technician <= self.T
            or self.n > 0
        ):

            self.time = self.time_departure_specialized_technician
            client = self.specialized_technician
            self.profits += self.cost[client]
            self.departure_count+=1
            self.departure[self.departure_count] = self.time
            self.n-=1

            if self.technicians_queue:
                try:
                    self.technicians_queue.remove(3)
                    self.specialized_technician = 3
                except ValueError:
                    self.specialized_technician = self.technicians_queue.popleft()
                self.time_departure_specialized_technician = self.time + exponential(1/15)
            else:
                self.time_departure_specialized_technician = float("inf")


