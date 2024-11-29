import unittest
import time
from a_para_la_busqueda_del_tesoro import a_star_treasure_hunt
from adversarySeach import alpha_beta_treasure_hunt

class TestPerformance(unittest.TestCase):

    def test_performance_a_star(self):
        grid = [['0'] * 50 for _ in range(50)]
        grid[0][0] = 'S'
        grid[49][49] = 'T'
        start_time = time.time()
        path = a_star_treasure_hunt(grid)
        end_time = time.time()
        self.assertIsNotNone(path)
        print(f"A* Time: {end_time - start_time} seconds")

    def test_performance_minimax(self):
        grid = [['0'] * 50 for _ in range(50)]
        grid[0][0] = 'S'
        grid[49][49] = 'T'
        start_time = time.time()
        player_path, guard_paths = alpha_beta_treasure_hunt(grid)
        end_time = time.time()
        self.assertIsNotNone(player_path)
        print(f"Minimax Time: {end_time - start_time} seconds")

if __name__ == '__main__':
    unittest.main()