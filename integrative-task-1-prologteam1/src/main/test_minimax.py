# test_minimax.py
import unittest
from adversarySeach import alpha_beta_treasure_hunt

class TestAlphaBetaTreasureHunt(unittest.TestCase):

    def test_basic_functionality(self):
        grid = [
            ['S', '.', 'G'],
            ['.', '#', '.'],
            ['.', '.', 'T']
        ]
        expected_player_path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        player_path, guard_paths = alpha_beta_treasure_hunt(grid)
        self.assertIsNotNone(player_path)
        self.assertEqual(player_path, expected_player_path)

    def test_no_path(self):
        grid = [
            ['S', '#', '#'],
            ['#', '#', '#'],
            ['#', '#', 'T']
        ]
        expected_player_path = [(0, 0)]
        player_path, guard_paths = alpha_beta_treasure_hunt(grid)
        self.assertIsNotNone(player_path)
        self.assertEqual(player_path, expected_player_path)

    def test_edge_case_guard_near(self):
        grid = [
            ['S', '.', '.'],
            ['.', 'G', '.'],
            ['.', '.', 'T']
        ]
        expected_player_path = [(0, 0), (0, 1)]
        player_path, guard_paths = alpha_beta_treasure_hunt(grid)
        self.assertIsNotNone(player_path)
        self.assertEqual(player_path, expected_player_path)

if __name__ == '__main__':
    unittest.main()