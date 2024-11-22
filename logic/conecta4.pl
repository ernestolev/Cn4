% Reglas básicas para el juego de Conecta 4.

% Representación del tablero:
% Es una lista de listas de tamaño 6x7. Cada posición puede contener:
% - " " para vacío
% - "rojo" para jugador 1
% - "amarillo" para jugador 2

% Verificar si una columna está llena
columna_llena(Tablero, Columna) :-
    nth0(0, Tablero, FilaSuperior),
    nth0(Columna, FilaSuperior, Celda),
    Celda \= " ".

% Generar jugadas válidas (columnas no llenas)
jugadas_validas(Tablero, Jugadas) :-
    findall(C, (between(0, 6, C), \+ columna_llena(Tablero, C)), Jugadas).

% Insertar ficha en una columna
insertar_ficha(Tablero, Columna, Ficha, NuevoTablero) :-
    nth0(Columna, Tablero, ColumnaActual),
    encontrar_fila_disponible(ColumnaActual, Fila),
    reemplazar_fila(Tablero, Columna, Fila, Ficha, NuevoTablero).

% Encontrar la fila disponible en una columna
encontrar_fila_disponible(Columna, Fila) :-
    reverse(Columna, Reversa),
    nth0(Index, Reversa, " "),
    length(Columna, Total),
    Fila is Total - Index - 1.

% Reemplazar una celda en el tablero
reemplazar_fila(Tablero, Columna, Fila, Ficha, NuevoTablero) :-
    nth0(Columna, Tablero, ColumnaActual),
    reemplazar_en_lista(ColumnaActual, Fila, Ficha, NuevaColumna),
    reemplazar_en_lista(Tablero, Columna, NuevaColumna, NuevoTablero).

% Reemplazar un elemento en una lista
reemplazar_en_lista([_|T], 0, Elem, [Elem|T]).
reemplazar_en_lista([H|T], Index, Elem, [H|NT]) :-
    Index > 0,
    NewIndex is Index - 1,
    reemplazar_en_lista(T, NewIndex, Elem, NT).

% Verificar si hay un ganador
hay_ganador(Tablero, Ficha) :-
    hay_linea_horizontal(Tablero, Ficha);
    hay_linea_vertical(Tablero, Ficha);
    hay_linea_diagonal(Tablero, Ficha).

% Verificar líneas horizontales
hay_linea_horizontal(Tablero, Ficha) :-
    member(Fila, Tablero),
    sublista(Ficha, Fila).

% Verificar líneas verticales
hay_linea_vertical(Tablero, Ficha) :-
    transpose(Tablero, TableroT),
    member(Columna, TableroT),
    sublista(Ficha, Columna).

% Verificar líneas diagonales
hay_linea_diagonal(Tablero, Ficha) :-
    diagonales(Tablero, Diagonales),
    member(Diagonal, Diagonales),
    sublista(Ficha, Diagonal).

% Verificar si una sublista contiene 4 elementos consecutivos iguales
sublista(Ficha, Lista) :-
    append(_, [Ficha, Ficha, Ficha, Ficha|_], Lista).

% Generar diagonales del tablero
diagonales(Tablero, Diagonales) :-
    findall(D, diagonal(Tablero, D), Diagonales).

% IA: Escoge una jugada válida al azar (puedes mejorar esto con heurísticas)
jugada_ia(Tablero, Ficha, Columna, Fila) :-
    jugadas_validas(Tablero, Jugadas),
    random_member(Columna, Jugadas),
    insertar_ficha(Tablero, Columna, Ficha, NuevoTablero),
    encontrar_fila_disponible(NuevoTablero, Columna, Fila).
