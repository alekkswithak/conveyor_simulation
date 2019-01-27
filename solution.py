from enum import Enum
import random

class Worker:
    """
    Represents a worker on a slot
    """

    def __init__(self):
        self.items = []
        self.time = 4
        self.working = False

    def __repr__(self):
        return '<Worker>'

    def got_both(self):
        """
        Checks if worker has both component items
        :return:
        """
        if Item.A in self.items and Item.B in self.items:
            return True

    def take_item(self, item):
        """
        Takes item from slot
        Initiates work if has both types of component
        """
        if len(self.items) <= 2:
            self.items.append(item)
            if self.got_both():
                self.working = True

    def work(self):
        """
        Workers assembling the product
        """
        if self.working:
            if self.time == 0:
                self.items = [Item.P]
                self.working = False
                self.time = 4
            else:
                self.time -= 1


class Item(Enum):
    """
    Represents one of 4 states of a possible item
    """

    E = 0 # represents an empty slot
    A = 1 # represents component A
    B = 2 # represents component B
    P = 3 # represents product P

    @classmethod
    def random(cls):
        return random.choice([Item.E, Item.A, Item.B])


class Slot:
    """
    Represents a slot on the conveyor
    """
    def __init__(self):
        self.item = Item.E
        self.workers = [Worker(), Worker()]

    def __repr__(self):
        return '<Slot: {}>'.format(self.item.name)

    def work(self):
        """
        Carries out the work for each iteration
        Places a product p if any workers have it ready
        Or has a worker take the item if one needs it
        Increments the remaining workers work time
        """
        worker = self.worker_place_item()
        if not worker:
            worker = self.worker_take_item()

        if not worker:
            for worker in self.workers:
                worker.work()
        else:
            worker = [w for w in self.workers if w is not worker][0]
            worker.work()

    def worker_place_item(self):
        """
        If any workers have P, they will place it
        and return True, else None
        """
        if self.item == Item.E:
            worker = self.get_ready_worker()
            if worker:
                worker.items.remove(Item.P)
                self.item = Item.P
                return worker

    def worker_take_item(self):
        """
        If a worker is waiting for the item in the slot
        They take it and replace it with the empty item
        """
        worker = self.get_waiting_worker()
        if worker:
            worker.take_item(self.item)
            self.item = Item.E
            return worker

    def get_waiting_worker(self):
        """
        Returns the first worker who is not working
        and does not have self.item
        """
        if self.item in (Item.A, Item.B):
            for worker in self.workers:
                if not worker.working and self.item not in worker.items:
                    return worker

    def get_ready_worker(self):
        """
        Returns a worker with Item.P or none
        """
        for worker in self.workers:
            if Item.P in worker.items:
                return worker


class Conveyor:

    def __init__(self, length=5):
        self.slots = [Slot() for _ in range(length)]
        self.length = length
        self.outputs = []

    def __repr__(self):
        return '<Conveyor>'

    def run(self):
        """
        Runs the work on each slot and increments the conveyor
        """
        for slot in self.slots:
            slot.work()
        self.increment()

    def increment(self):
        """
        Moves items along the slots of the conveyor
        """
        self.add_output()
        for i in range(self.length-1, 0, -1):
            self.slots[i].item = self.slots[i-1].item
        self.slots[0].item = Item.random()

    def add_output(self):
        """
        Adds all non empty items to the conveyor output
        """
        if self.slots[self.length-1].item is not Item.E:
            self.outputs.append(self.slots[self.length-1].item)


def simulate(times=100):
    """
    Runs the conveyor over 100 iterations as default
    Returns the amount of products made
    """
    conveyor = Conveyor()
    conveyor.slots[0].item = Item.random()
    for _ in range(times):
        conveyor.run()
    return len([i for i in conveyor.outputs if i == Item.P])


def simulate_monte_carlo(times=1000):
    """
    Runs the simulation 1000 times as default
    Prints the average
    """
    print(sum(simulate() for _ in range(times))/times)


if __name__ == '__main__':
    simulate_monte_carlo()
