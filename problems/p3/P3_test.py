import unittest
import io
import random
import os

from SectorMap import SectorMap
from PriorityQueue import PriorityQueue

class TestPriorityQueue(unittest.TestCase):
    def test_priority_queue(self):
        random.seed(1)
        test_list = [[x,x] for x in range(-100,100)]
        random.shuffle(test_list)

        pq = PriorityQueue(test_list)

        i = -100
        while len(pq) > 0:
            e = pq.pop()
            self.assertEqual(e, i, "PriorityQueue did not sort correctly.")
            i += 1

    def test_handles_empty_pop(self):
        pq = PriorityQueue([[1,1]])
        pq.pop()
        self.assertEqual(pq.pop(), None, "Failed to return None on popping empty Priority Queue")
            

class TestP3(unittest.TestCase):
    #@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    #def test_sector_read(self, mock_stout):

    TEST_GRAPH = """c 1 2 14
c 2 5 12
c 1 3 17
c 3 5 19
c 5 9 14
c 9 10 18
c 10 4 12
c 10 11 20
c 11 14 10
c 9 12 10
c 14 12 20
c 12 15 14
c 15 16 11
c 12 8 10
c 8 13 16
c 8 6 20
c 6 7 12"""

    def loadGraph(self, data):
        with open("sector.dat", "w") as f:
            f.write(data)
        self.graph = SectorMap("sector.dat")
        os.remove("sector.dat")

    def test_edge_read(self):
        self.loadGraph(self.TEST_GRAPH)
        self.assertEqual(self.graph.get_length(1, 2), 14, "Failed to find edge.")
        self.assertEqual(self.graph.get_length(2, 1), 14, "Failed to find edge.")
        self.assertEqual(self.graph.get_length(16, 1), None, "Failed to find edge.")
        self.assertEqual(self.graph.get_length(16, 15), 11, "Failed to find edge.")

    def test_edge_modify(self):
        self.loadGraph(self.TEST_GRAPH)
        self.assertEqual(self.graph.get_length(1, 2), 14, "Failed to find edge.")
        self.graph.set_length(1,2,10)
        self.assertEqual(self.graph.get_length(1, 2), 10, "Failed to change edge length.")
        self.assertEqual(self.graph.get_length(2, 1), 10, "Failed to change edge length.")

    def test_jarnik(self):
        self.loadGraph(self.TEST_GRAPH)
        nodes = self.graph.jarnik()
        self.assertEqual(nodes, [(1, 2), (2, 5), (5, 9), (9, 12), (12, 8), (12, 15), (15, 16), (8, 13), (1, 3), (9, 10), (10, 4), (12, 14), (14, 11), (8, 6), (6, 7)], "Jarnik did not construct tree correctly.")

    def test_dijkstra(self):
        self.loadGraph(self.TEST_GRAPH)
        nodes = self.graph.dijkstra(16, 1)
        self.assertEqual(nodes, [16,15,12,9,5,2,1], "Dijkstra found incorrect path.")

if __name__ == '__main__':
    unittest.main()



