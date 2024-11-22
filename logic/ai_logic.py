import random

class Conecta4AI:
    def __init__(self, color):
        """
        Inicializa la IA con el color de las fichas que manejará.
        :param color: "rojo" o "amarillo"
        """
        self.color = color

    def obtener_jugada(self, tablero):
        """
        Calcula la mejor jugada disponible.
        :param tablero: Tablero actual del juego (lista de listas).
        :return: Índice de la columna donde colocar la ficha.
        """
        columnas_validas = self.columnas_validas(tablero)
        
        # Evaluar si hay una jugada ganadora
        for columna in columnas_validas:
            if self.es_jugada_ganadora(tablero, columna):
                return columna

        # Evaluar si hay que bloquear al oponente
        oponente = "rojo" if self.color == "amarillo" else "amarillo"
        for columna in columnas_validas:
            if self.es_jugada_ganadora(tablero, columna, ficha=oponente):
                return columna

        # Si no hay jugadas inmediatas, elige al azar
        return random.choice(columnas_validas)

    def columnas_validas(self, tablero):
        """
        Devuelve una lista de índices de las columnas que no están llenas.
        :param tablero: Tablero actual del juego.
        :return: Lista de índices de columnas disponibles.
        """
        return [c for c in range(7) if tablero[0][c] == " "]

    def es_jugada_ganadora(self, tablero, columna, ficha=None):
        """
        Determina si colocar una ficha en una columna específica resulta en una victoria.
        :param tablero: Tablero actual del juego.
        :param columna: Índice de la columna a probar.
        :param ficha: Color de la ficha a usar ("rojo" o "amarillo").
        :return: True si resulta en victoria, False en caso contrario.
        """
        if ficha is None:
            ficha = self.color

        # Clonar el tablero y simular la jugada
        tablero_simulado = [fila[:] for fila in tablero]
        fila = self.encontrar_fila_disponible(tablero_simulado, columna)
        if fila is None:
            return False

        tablero_simulado[fila][columna] = ficha
        return self.hay_ganador(tablero_simulado, fila, columna, ficha)

    def encontrar_fila_disponible(self, tablero, columna):
        """
        Encuentra la primera fila vacía en una columna.
        :param tablero: Tablero actual del juego.
        :param columna: Índice de la columna.
        :return: Índice de la fila disponible o None si la columna está llena.
        """
        for fila in range(5, -1, -1):
            if tablero[fila][columna] == " ":
                return fila
        return None

    def hay_ganador(self, tablero, fila, columna, ficha):
        """
        Verifica si la jugada en (fila, columna) genera un ganador.
        :param tablero: Tablero actual del juego.
        :param fila: Fila de la jugada.
        :param columna: Columna de la jugada.
        :param ficha: Color de la ficha a verificar.
        :return: True si hay un ganador, False en caso contrario.
        """
        return (
            self.verificar_direccion(tablero, fila, columna, ficha, 1, 0) or  # Horizontal
            self.verificar_direccion(tablero, fila, columna, ficha, 0, 1) or  # Vertical
            self.verificar_direccion(tablero, fila, columna, ficha, 1, 1) or  # Diagonal \
            self.verificar_direccion(tablero, fila, columna, ficha, 1, -1)    # Diagonal /
        )

    def verificar_direccion(self, tablero, fila, columna, ficha, dx, dy):
        """
        Verifica si hay 4 fichas consecutivas en una dirección específica.
        :param tablero: Tablero actual del juego.
        :param fila: Fila inicial.
        :param columna: Columna inicial.
        :param ficha: Color de la ficha a verificar.
        :param dx: Dirección en filas.
        :param dy: Dirección en columnas.
        :return: True si hay 4 consecutivas, False en caso contrario.
        """
        count = 0
        for step in range(-3, 4):
            x, y = fila + step * dx, columna + step * dy
            if 0 <= x < 6 and 0 <= y < 7 and tablero[x][y] == ficha:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False
