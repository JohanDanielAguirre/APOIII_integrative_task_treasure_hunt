# test_integration.py
import unittest
from a_para_la_busqueda_del_tesoro import a_star_treasure_hunt
from adversarySeach import alpha_beta_treasure_hunt

class TestIntegration(unittest.TestCase):

    def test_integration_a_star(self):
        grid = [
            ['S', '.', '.'],
            ['.', '#', '.'],
            ['.', '.', 'T']
        ]
        expected_path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
        path = a_star_treasure_hunt(grid)
        self.assertIsNotNone(path)
        self.assertEqual(path, expected_path)

    def test_integration_minimax(self):
        grid = [
            ['S', '.', '.', '.'],
            ['#', '.', '#', 'G'],
            ['.', '.', '.', '#'],
            ['T', '.', '.', '.']
        ]
        expected_player_path = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (3,0)]
        player_path, guard_paths = alpha_beta_treasure_hunt(grid)
        self.assertIsNotNone(player_path)
        self.assertEqual(player_path, expected_player_path)

if __name__ == '__main__':
    unittest.main()