import unittest
from solution import (
    Worker,
    Item,
    Slot,
    Conveyor,
)

class TestWorker(unittest.TestCase):

    def test_got_both(self):
        w = Worker()
        items = [Item.A, Item.B]
        w.items.extend(items)
        self.assertTrue(w.got_both())

    def test_take_item_a(self):
        w = Worker()
        w.take_item(Item.A)
        self.assertTrue(Item.A in w.items)
        self.assertFalse(w.working)

    def test_take_item_a_and_b(self):
        w = Worker()
        w.take_item(Item.A)
        w.take_item(Item.B)
        self.assertTrue(all(i in w.items for i in (Item.A, Item.B)))
        self.assertTrue(w.working)


class TestSlot(unittest.TestCase):

    def test_get_worker_item_a(self):
        s = Slot()
        s.item = Item.A
        w = s.get_waiting_worker()
        self.assertTrue(w)

    def test_get_worker_item_e(self):
        s = Slot()
        w = s.get_waiting_worker()
        self.assertFalse(w)

    def test_get_worker_both_working(self):
        s = Slot()
        for w in s.workers:
            w.working = True
        w = s.get_waiting_worker()
        self.assertFalse(w)

    def test_ready_worker(self):
        s = Slot()
        s.workers[0].items.append(Item.P)
        self.assertTrue(s.get_ready_worker())

    def test_no_ready_workers(self):
        s = Slot()
        self.assertFalse(s.get_ready_worker())


class TestConveyor(unittest.TestCase):

    def test_add_output_e(self):
        c = Conveyor()
        c.add_output()
        self.assertFalse(c.outputs)

    def test_add_output_not_e(self):
        c = Conveyor()
        c.slots[4].item = Item.A
        c.add_output()
        self.assertTrue(c.outputs)


if __name__ == '__main__':
    unittest.main()