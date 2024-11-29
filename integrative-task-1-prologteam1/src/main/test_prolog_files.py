# test_prolog_files.py
import unittest
import subprocess
from pathlib import Path

class TestPrologFiles(unittest.TestCase):

    def test_prolog_constraints(self):
        prolog_source = Path("programming with constraints.pl")
        if not prolog_source.exists():
            self.fail(f"No se encuentra el archivo: {prolog_source}")

        cmd = [
            "swipl",
            "-s", str(prolog_source),
            "-g", "halt."
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Error en la ejecución: {result.stderr}")

    def test_prolog_maze(self):
        maze_file = Path("maze_prolog.pl")
        if not maze_file.exists():
            self.fail(f"No se encuentra el archivo: {maze_file}")

        cmd = [
            "swipl",
            "-s", str(maze_file),
            "-g", "halt."
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Error en la ejecución: {result.stderr}")

if __name__ == '__main__':
    unittest.main()