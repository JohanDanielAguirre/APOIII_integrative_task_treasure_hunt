% Consultar el archivo maze_prolog.pl
:- consult('maze_prolog.pl').

% Reglas de movimiento 
move(up, X, Y, X1, Y) :- 
    X1 is X - 1, 
    X1 >= 0, 
    cell(X1, Y, Type), 
    Type \= obstacle, 
    Type \= guard.

move(down, X, Y, X1, Y) :- 
    X1 is X + 1, 
    cell(X1, Y, Type), 
    Type \= obstacle, 
    Type \= guard.

move(left, X, Y, X, Y1) :- 
    Y1 is Y - 1, 
    Y1 >= 0, 
    cell(X, Y1, Type), 
    Type \= obstacle, 
    Type \= guard.

move(right, X, Y, X, Y1) :- 
    Y1 is Y + 1, 
    cell(X, Y1, Type), 
    Type \= obstacle, 
    Type \= guard.

% DFS con control de celdas visitadas
dfs(X, Y, [(X, Y)], _) :-
    cell(X, Y, treasure),  % Caso base: si encontramos el tesoro, terminamos
    writeln('Tesoro encontrado en:'), writeln((X, Y)).

dfs(X, Y, [(X, Y) | Path], Visited) :-
    move(_, X, Y, X1, Y1),          % Intentamos movernos en alguna dirección
    \+ member((X1, Y1), Visited),   % Verificamos que no hayamos visitado esa celda
    writeln('Moviéndonos a:'), writeln((X1, Y1)),
    dfs(X1, Y1, Path, [(X1, Y1) | Visited]). 

% Encuentra la posición inicial
find_start(X, Y) :-
    cell(X, Y, start),
    writeln('Inicio en:'), writeln((X, Y)).


% Inicia la búsqueda desde la posición de start
find_treasure(Path) :-
    find_start(X, Y),
    dfs(X, Y, Path, [(X, Y)]).
