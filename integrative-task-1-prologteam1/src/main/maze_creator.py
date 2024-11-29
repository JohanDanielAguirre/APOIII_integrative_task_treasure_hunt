import tkinter as tk
from pathlib import Path
from tkinter import simpledialog, messagebox
import subprocess
from heapq import heappop, heappush

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Creator")
        self.grid = []
        self.rows = 0
        self.cols = 0
        self.prolog_path = Path(r"C:\Program Files\swipl\bin\swipl.exe")
        if not self.verify_prolog_installation():
            messagebox.showerror("Error", "No se encontró SWI-Prolog en la ruta esperada.")
        self.create_widgets()

    def verify_prolog_installation(self):
        """Verifica que SWI-Prolog esté instalado y sea accesible."""
        try:
            if not self.prolog_path.exists():
                return False

            result = subprocess.run(
                [str(self.prolog_path), "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    def create_widgets(self):
        self.row_label = tk.Label(self.root, text="Rows:")
        self.row_label.grid(row=0, column=0)
        self.row_entry = tk.Entry(self.root)
        self.row_entry.grid(row=0, column=1)

        self.col_label = tk.Label(self.root, text="Columns:")
        self.col_label.grid(row=1, column=0)
        self.col_entry = tk.Entry(self.root)
        self.col_entry.grid(row=1, column=1)

        self.create_button = tk.Button(self.root, text="Create Maze", command=self.create_maze)
        self.create_button.grid(row=2, column=0, columnspan=2)

    def create_maze(self):
        while True:
            try:
                self.rows = int(self.row_entry.get())
                self.cols = int(self.col_entry.get())
                if self.rows <= 0 or self.cols <= 0:
                    raise ValueError("Dimensions must be positive")
                break  # Exit the loop if dimensions are valid
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                continue  # Prompt the user again

        self.grid = [['' for _ in range(self.cols)] for _ in range(self.rows)]

        valid_cell_types = {'S', 'T', '#', '.', 'G'}
        start_placed = False
        treasure_placed = False

        for i in range(self.rows):
            for j in range(self.cols):
                cell_type = None
                while cell_type not in valid_cell_types:
                    cell_type = simpledialog.askstring("Input", f"Enter cell type for ({i}, {j}) [S/T/#/./G]:")
                    if cell_type not in valid_cell_types:
                        messagebox.showerror("Error", "Invalid cell type. Please enter one of [S, T, #, ., G].")
                    elif cell_type == 'S' and start_placed:
                        messagebox.showerror("Error", "Start (S) already placed. Please choose another cell type.")
                        cell_type = None
                    elif cell_type == 'T' and treasure_placed:
                        messagebox.showerror("Error", "Treasure (T) already placed. Please choose another cell type.")
                        cell_type = None

                if cell_type == 'S':
                    start_placed = True
                elif cell_type == 'T':
                    treasure_placed = True

                self.grid[i][j] = cell_type
                self.draw_cell(i, j, cell_type)

        self.save_button = tk.Button(self.root, text="Save and Solve", command=self.save_and_solve)
        self.save_button.grid(row=self.rows + 3, column=0, columnspan=self.cols)

    def draw_cell(self, row, col, cell_type):
        color = {
            'S': 'green',
            'T': 'gold',
            '#': 'black',
            '.': 'white',
            'G': 'red'
        }.get(cell_type, 'white')
        cell = tk.Label(self.root, text=cell_type, bg=color, width=4, height=2, borderwidth=1, relief="solid")
        cell.grid(row=row + 3, column=col)  # Offset by 3 to avoid overlap with input widgets

    def save_and_solve(self):
        try:
            self.save_maze_to_file("maze.txt")
            self.save_maze_to_prolog_file("maze_prolog.pl")
            self.show_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el laberinto: {str(e)}")

    def save_maze_to_file(self, filename):
        current_dir = Path(__file__).parent
        file_path = current_dir / filename
        with open(file_path, 'w') as file:
            for row in self.grid:
                file.write(' '.join(row) + '\n')

    def save_maze_to_prolog_file(self, filename):
        current_dir = Path(__file__).parent
        file_path = current_dir / filename
        with open(file_path, 'w') as file:
            # Escribir dimensiones del laberinto
            file.write(f"maze_size({self.rows}, {self.cols}).\n\n")

            for i, row in enumerate(self.grid):
                for j, cell in enumerate(row):
                    if cell == 'S':
                        file.write(f"cell({i}, {j}, start).\n")
                    elif cell == 'T':
                        file.write(f"cell({i}, {j}, treasure).\n")
                    elif cell == '#':
                        file.write(f"cell({i}, {j}, obstacle).\n")
                    elif cell == 'G':
                        file.write(f"cell({i}, {j}, guard).\n")
                    elif cell == '.':
                        file.write(f"cell({i}, {j}, empty).\n")


    def show_menu(self):
        while True:
            print("Métodos disponibles:\n",
                  "1. Lógica de programación (Prolog)\n",
                  "2. Programación lógica con restricciones (CLP)\n",
                  "3. Búsqueda heurística (A*)\n",
                  "4. Búsqueda adversaria (Minimax)\n",
                  "5. Salir\n")
            choice = int(input("Selecciona el método (1-5): "))
            if choice == 1:
                self.solve_with_prolog()
            elif choice == 2:
                self.solve_with_clp()
            elif choice == 3:
                self.solve_with_a_star()
            elif choice == 4:
                self.solve_with_minimax()
            elif choice == 5:
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")

    def solve_with_prolog(self):
        if not self.verify_prolog_installation():
            messagebox.showerror("Error", "SWI-Prolog no está disponible.")
            return

        try:
            current_dir = Path(__file__).parent
            prolog_source = current_dir / "logic programming solve.pl"
            maze_file = current_dir / "maze_prolog.pl"

            # Verificar que los archivos existen
            if not prolog_source.exists():
                messagebox.showerror("Error", f"No se encuentra el archivo: {prolog_source}")
                return
            if not maze_file.exists():
                messagebox.showerror("Error", f"No se encuentra el archivo: {maze_file}")
                return

            # Ejecutar Prolog con la ruta completa
            cmd = [
                str(self.prolog_path),
                "-s", str(prolog_source),
                "-g", "find_treasure(Path),halt."
            ]

            print(f"Ejecutando comando: {' '.join(cmd)}")  # Para depuración

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(current_dir)  # Establecer el directorio de trabajo
            )

            print("Salida estándar de Prolog:", result.stdout)
            print("Salida de error de Prolog:", result.stderr)

            if result.returncode == 0:
                if result.stdout.strip():
                    messagebox.showinfo("Éxito", f"Solución encontrada:\n{result.stdout}")
                else:
                    messagebox.showwarning("Aviso", "No se encontró solución")
            else:
                error_msg = result.stderr if result.stderr else "Error desconocido al ejecutar Prolog"
                messagebox.showerror("Error", f"Error en la ejecución:\n{error_msg}")

        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "La ejecución de Prolog excedió el tiempo límite")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def solve_with_clp(self):
        if not self.verify_prolog_installation():
            messagebox.showerror("Error", "SWI-Prolog no está disponible.")
            return

        try:
            current_dir = Path(__file__).parent
            prolog_source = current_dir / "programming with constraints.pl"
            maze_file = current_dir / "maze_prolog.pl"

            # Verificar que los archivos existen
            if not prolog_source.exists():
                messagebox.showerror("Error", f"No se encuentra el archivo: {prolog_source}")
                return
            if not maze_file.exists():
                messagebox.showerror("Error", f"No se encuentra el archivo: {maze_file}")
                return

            max_moves = simpledialog.askinteger("Input",
                                                "Número máximo de movimientos permitidos:",
                                                initialvalue=self.rows * self.cols,  # Valor inicial basado en el tamaño del laberinto
                                                minvalue=1,
                                                maxvalue=self.rows * self.cols * 2)  # Máximo razonable

            if max_moves is None:
                return

            # Ejecutar Prolog con la ruta completa
            cmd = [
                str(self.prolog_path),
                "-s", str(prolog_source),
                "-g", f"find_treasure(Path,{max_moves}),halt."
            ]

            print(f"Ejecutando comando: {' '.join(cmd)}")  # Para depuración

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(current_dir)  # Establecer el directorio de trabajo
            )

            print("Salida estándar de Prolog:", result.stdout)
            print("Salida de error de Prolog:", result.stderr)

            if result.returncode == 0:
                if result.stdout.strip():
                    messagebox.showinfo("Éxito", f"Solución encontrada:\n{result.stdout}")
                else:
                    messagebox.showwarning("Aviso", "No se encontró solución")
            else:
                error_msg = result.stderr if result.stderr else "Error desconocido al ejecutar Prolog"
                messagebox.showerror("Error", f"Error en la ejecución:\n{error_msg}")

        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "La ejecución de Prolog excedió el tiempo límite")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def solve_with_a_star(self):
        from a_para_la_busqueda_del_tesoro import a_star_treasure_hunt
        with open("maze.txt", 'r') as file:
            grid = [line.strip().split() for line in file]
        path = a_star_treasure_hunt(grid)
        if path:
            self.draw_path_a(path)
    def draw_path_a(self, path):
        path_window = tk.Toplevel(self.root)
        path_window.title("Path Found")

        for (row, col) in path:
            cell = tk.Label(path_window, text='P', bg='blue', width=4, height=2, borderwidth=1, relief="solid")
            cell.grid(row=row, column=col)

    def draw_path(self, player_path, guard_paths):
        path_window = tk.Toplevel(self.root)
        path_window.title("Path Found minmax")

        # Dibujar el recorrido del jugador en azul
        for (row, col) in player_path:
            cell = tk.Label(path_window, text='P', bg='blue', width=4, height=2, borderwidth=1, relief="solid")
            cell.grid(row=row, column=col)

        # Dibujar el recorrido de los guardias en rojo
        for guard_path in guard_paths:
            for (row, col) in guard_path:
                cell = tk.Label(path_window, text='G', bg='red', width=4, height=2, borderwidth=1, relief="solid")
                cell.grid(row=row, column=col)

    def solve_with_minimax(self):
        from adversarySeach import alpha_beta_treasure_hunt
        with open("maze.txt", 'r') as file:
            grid = [line.strip().split() for line in file]
        player_path, guard_paths = alpha_beta_treasure_hunt(grid)
        if player_path and guard_paths:
            self.draw_path(player_path, guard_paths)


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()