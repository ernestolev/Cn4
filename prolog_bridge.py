from pyswip import Prolog

class PrologBridge:
    def __init__(self):
        """Inicializa la conexión con Prolog."""
        self.prolog = Prolog()
        try:
            # Consulta el archivo Prolog que contiene la lógica del juego
            self.prolog.consult("logic/conecta4.pl")
        except Exception as e:
            print(f"Error al cargar conecta4.pl: {e}")

    def jugada_ia(self, tablero, color):
        """
        Calcula la jugada de la IA usando Prolog.
        :param tablero: Tablero actual del juego como lista de listas.
        :param color: Color de la ficha de la IA ("amarillo" o "rojo").
        :return: (columna, fila) de la jugada, o None si no hay jugada posible.
        """
        # Convertir el tablero a un formato compatible con Prolog
        tablero_prolog = self.tablero_a_prolog(tablero)
        query = f"jugada_ia({tablero_prolog}, '{color}', Columna, Fila)"
        
        try:
            resultado = list(self.prolog.query(query))
            if resultado:
                return int(resultado[0]["Columna"]), int(resultado[0]["Fila"])
        except Exception as e:
            print(f"Error al ejecutar jugada_ia: {e}")
        
        return None

    @staticmethod
    def tablero_a_prolog(tablero):
        """
        Convierte el tablero de Python (listas de listas) a un formato de Prolog.
        :param tablero: Tablero como lista de listas.
        :return: Representación del tablero como string compatible con Prolog.
        """
        # Convertir listas de Python a listas de Prolog
        return str(tablero).replace("'", '"')
