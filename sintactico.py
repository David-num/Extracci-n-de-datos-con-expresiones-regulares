# Analizador sintactico
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def obtener_token_actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def coincidir(self, tipo_esperado):
        token_actual = self.obtener_token_actual()
        if token_actual and token_actual[0] == tipo_esperado:
            self.pos += 1
            return token_actual
        else:
            raise SyntaxError(f'Error sintactico: se esperaba {tipo_esperado}, pero se encontro: {token_actual}')

    def parsear(self):
        # Punto de entrada: se epera una funcion
        self.funcion()

    def funcion(self):
        # Gramatica para una funcion: int IDENTIFIER (int IDENTIFIER) {cuerpo}
        self.coincidir('KEYWORD') # Tipo de retorno (ej. int)
        self.coincidir('IDENTIFIER') # Nombre de la funcion
        self.coincidir('DELIMITER') # Se espera un (
        self.parametros() # Regla para los parametros
        self.coincidir('DELIMITER') # Se espera un )
        self.coincidir('DELIMITER') # Se espera un {
        self.cuerpo() # Regla parael cuerpo de la funcino
        self.coincidir('DELIMITER') # Se espera un }

    def parametros(self):
        # Reglas para parametros: int IDENTIFIER (, int IDENTIFIER)*
        self.coincidir('KEYWORD') # Tipo de parametro
        self.coincidir('IDENTIFIER') # Nombre del parametro
        while self.obtener_token_actual() and self.obtener_token_actual()[1] == ',': 
            self.coincidir('DELIMITER') # Se espera una ,
            self.coincidir('KEYWORD') # Tipo de parametro
            self.coincidir('IDENTIFIER') # Nombre del parametro

    def cuerpo(self):
        # Gramatica para el cuerpo: return IDENTIFIER OPERATOR IDENTIFIER:
        self.coincidir('KEYWORD') # Se espera un return
        self.coincidir('IDENTIFIER') # <Nombre de la variable>
        self.coincidir('OPERATOR') # Operador ej: +
        self.coincidir('IDENTIFIER') # <Nombre de la variable>
        self.coincidir('DELIMITER') # Se espera un ;
    