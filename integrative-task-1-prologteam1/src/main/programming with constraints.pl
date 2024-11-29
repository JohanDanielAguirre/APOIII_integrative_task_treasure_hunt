:- use_module(library(clpfd)).

% Consultar el archivo maze_prolog.pl para obtener las dimensiones y el estado del laberinto
:- consult('maze_prolog.pl').

% Reglas de movimiento usando restricciones
move(up, X, Y, X1, Y) :-
    maze_size(MaxX, MaxY),
    X1 #= X - 1,
    X1 #>= 0,
    X1 #< MaxX,
    Y #>= 0, Y #< MaxY,
    cell(X1, Y, Type),
    Type \= obstacle,
    Type \= guard.

move(down, X, Y, X1, Y) :-
    maze_size(MaxX, MaxY),
    X1 #= X + 1,
    X1 #>= 0,
    X1 #< MaxX,
    Y #>= 0, Y #< MaxY,
    cell(X1, Y, Type),
    Type \= obstacle,
    Type \= guard.

move(left, X, Y, X, Y1) :-
    maze_size(MaxX, MaxY),
    Y1 #= Y - 1,
    Y1 #>= 0,
    Y1 #< MaxY,
    X #>= 0, X #< MaxX,
    cell(X, Y1, Type),
    Type \= obstacle,
    Type \= guard.

move(right, X, Y, X, Y1) :-
    maze_size(MaxX, MaxY),
    Y1 #= Y + 1,
    Y1 #>= 0,
    Y1 #< MaxY,
    X #>= 0, X #< MaxX,
    cell(X, Y1, Type), 
    Type \= obstacle, 
    Type \= guard.

% DFS con control de celdas visitadas y límite de movimientos usando restricciones
dfs(X, Y, Path, Visited, MovesLeft) :- 
    MovesLeft #> 0,                 % Aseguramos que aún hay movimientos
    cell(X, Y, treasure),            % Verificamos si la celda actual es el tesoro
    writeln('Tesoro encontrado en:'), writeln((X, Y)),
    Path = [(X, Y)].                 % Si sí, devolvemos el camino

dfs(X, Y, [(X, Y) | Path], Visited, MovesLeft) :- 
    MovesLeft #> 0,                 % Verifica si hay movimientos restantes
    move(_, X, Y, X1, Y1),          % Intentamos movernos en alguna dirección
    \+ member((X1, Y1), Visited),   % Verificamos que no hayamos visitado esa celda
    NewMovesLeft #= MovesLeft - 1,  % Reducimos el número de movimientos permitidos
    writeln('Moviéndonos a:'), writeln((X1, Y1)),
    writeln('Movimientos restantes:'), writeln(NewMovesLeft),  % Comentario de movimientos restantes
    dfs(X1, Y1, Path, [(X1, Y1) | Visited], NewMovesLeft). 

% Encuentra la posición inicial
find_start(X, Y) :- 
    cell(X, Y, start),
    writeln('Inicio en:'), writeln((X, Y)).

% Inicia la búsqueda desde la posición de start con un límite de movimientos usando restricciones
find_treasure(Path, MaxMoves) :- 
    MaxMoves #> 0,                        % Restricción: MaxMoves debe ser mayor que 0
    find_start(X, Y), 
    dfs(X, Y, Path, [(X, Y)], MaxMoves).  % Inicia la búsqueda con el máximo de movimientos permitido
