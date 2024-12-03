% conecta4.pl
:- dynamic board/1.
:- discontiguous check_winner/2.

% Inicializar el tablero vacío
init_board :-
    retractall(board(_)),
    assert(board([['_', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', '_', '_']])).

% Mostrar el tablero
display_board :-
    board(B),
    maplist(writeln, B).

% Insertar ficha en una columna desde abajo hacia arriba
insert_piece(Column, Player) :-
    board(Board),
    insert_in_column(Board, Column, Player, NewBoard),
    retract(board(Board)),
    assert(board(NewBoard)).

% Buscar la primera posición vacía desde abajo en una columna
insert_in_column(Board, Column, Player, NewBoard) :-
    find_empty_row(Board, Column, 1, RowIndex),
    set_piece(Board, RowIndex, Column, Player, NewBoard).

% Buscar la fila vacía en una columna
find_empty_row(Board, Column, CurrentRow, RowIndex) :-
    nth1(CurrentRow, Board, Row),
    nth1(Column, Row, Cell),
    Cell == '_', % Encuentra una celda vacía
    RowIndex = CurrentRow, !.
find_empty_row(Board, Column, CurrentRow, RowIndex) :-
    CurrentRow < 6, % No puede exceder las filas
    NextRow is CurrentRow + 1,
    find_empty_row(Board, Column, NextRow, RowIndex).

% Colocar una ficha en la posición especificada
set_piece(Board, Row, Column, Player, NewBoard) :-
    nth1(Row, Board, OldRow),
    replace_in_list(OldRow, Column, Player, NewRow),
    replace_in_list(Board, Row, NewRow, NewBoard).

% Reemplazar un elemento en una lista en una posición específica
replace_in_list([_|Rest], 1, Elem, [Elem|Rest]).
replace_in_list([Head|Rest], Pos, Elem, [Head|NewRest]) :-
    Pos > 1,
    NextPos is Pos - 1,
    replace_in_list(Rest, NextPos, Elem, NewRest).

% Verificar ganador (filas, columnas, diagonales)
check_winner(Player) :-
    board(Board),
    (check_rows(Board, Player, _);
     check_columns(Board, Player, _);
     check_diagonals(Board, Player, _)).

% Verificar ganador y obtener posiciones ganadoras
check_winner(Player, WinningPositions) :-
    board(Board),
    (check_rows(Board, Player, WinningPositions);
     check_columns(Board, Player, WinningPositions);
     check_diagonals(Board, Player, WinningPositions)).

check_rows(Board, Player, WinningPositions) :-
    nth1(RowIndex, Board, Row),
    check_sequence(Row, Player, RowIndex, 1, WinningPositions).

check_columns(Board, Player, WinningPositions) :-
    transpose(Board, Transposed),
    nth1(ColIndex, Transposed, Col),
    check_sequence(Col, Player, 1, ColIndex, WinningPositions).

check_diagonals(Board, Player, WinningPositions) :-
    diagonals(Board, Diagonals),
    nth1(DiagIndex, Diagonals, Diag),
    check_sequence(Diag, Player, DiagIndex, 1, WinningPositions).

check_sequence([A, B, C, D|_], Player, Row, Col, [(Row, Col), (Row, Col+1), (Row, Col+2), (Row, Col+3)]) :-
    A == Player, B == Player, C == Player, D == Player, !.
check_sequence([_|Rest], Player, Row, Col, WinningPositions) :-
    NextCol is Col + 1,
    check_sequence(Rest, Player, Row, NextCol, WinningPositions).

transpose([], []).
transpose([[]|_], []).
transpose(Board, [Row|Transposed]) :-
    maplist(nth1(1), Board, Row),
    maplist(remove_head, Board, RestBoard),
    transpose(RestBoard, Transposed).

remove_head([_|Tail], Tail).

diagonals(Board, Diagonals) :-
    findall(Diagonal, (diagonal(Board, Diagonal); diagonal_reverse(Board, Diagonal)), Diagonals).

diagonal(Board, Diagonal) :-
    length(Board, N),
    between(1, N, K),
    findall(Elem, (between(1, N, I), J is I + K - 1, nth1(I, Board, Row), nth1(J, Row, Elem)), Diagonal),
    length(Diagonal, L),
    L >= 4.

diagonal_reverse(Board, Diagonal) :-
    reverse(Board, ReversedBoard),
    diagonal(ReversedBoard, Diagonal).

% Movimiento de la computadora
computer_move :-
    board(Board),
    findall(Column, (between(1, 7, Column), can_insert_piece(Column)), ValidMoves),
    choose_best_move(Board, ValidMoves, Column),
    insert_piece(Column, 'Y').

% Elegir la mejor jugada
choose_best_move(Board, ValidMoves, BestMove) :-
    % Priorizar bloquear al jugador si tiene tres en línea
    (member(Move, ValidMoves), will_block_player(Board, Move) ->
        BestMove = Move
    ;
        % Si no hay necesidad de bloquear, elegir una jugada aleatoria
        random_member(BestMove, ValidMoves)
    ).

% Verificar si una jugada bloqueará al jugador
will_block_player(Board, Column) :-
    insert_in_column(Board, Column, 'R', NewBoard),
    check_winner('R', NewBoard).

% Verificar ganador en un tablero específico
check_winner(Player, Board) :-
    (check_rows(Board, Player, _);
     check_columns(Board, Player, _);
     check_diagonals(Board, Player, _)).

% Verificar si se puede insertar una ficha en una columna
can_insert_piece(Column) :-
    board(Board),
    nth1(6, Board, Row), % Verifica la fila superior
    nth1(Column, Row, Cell),
    Cell == '_'.

% Mejorar la lógica de detección de diagonales
diagonals(Board, Diagonals) :-
    findall(Diagonal, diagonal(Board, Diagonal), Diagonals1),
    findall(Diagonal, diagonal_reverse(Board, Diagonal), Diagonals2),
    append(Diagonals1, Diagonals2, Diagonals).

diagonal(Board, Diagonal) :-
    length(Board, N),
    between(1, N, K),
    findall(Elem, (between(1, N, I), J is I + K - 1, nth1(I, Board, Row), nth1(J, Row, Elem)), Diagonal),
    length(Diagonal, L),
    L >= 4.

diagonal_reverse(Board, Diagonal) :-
    reverse(Board, ReversedBoard),
    diagonal(ReversedBoard, Diagonal).