# test_a_star.py
import unittest
from a_para_la_busqueda_del_tesoro import a_star_treasure_hunt

class TestAStarTreasureHunt(unittest.TestCase):

    def test_basic_functionality(self):
        grid = [
            ['S', '.', '.'],
            ['.', '#', '.'],
            ['.', '.', 'T']
        ]
        expected_path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
        path = a_star_treasure_hunt(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path, expected_path)

    def test_no_path(self):
        grid = [
            ['S', '#', '#'],
            ['#', '#', '#'],
            ['#', '#', 'T']
        ]
        path = a_star_treasure_hunt(grid)
        self.assertIsNone(path)

    def test_edge_case_obstacles(self):
        grid = [
            ['S', '#', '#', '#', 'T'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.']
        ]
        expected_path = [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (0, 4)]
        path = a_star_treasure_hunt(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path, expected_path)

if __name__ == '__main__':
    unittest.main()