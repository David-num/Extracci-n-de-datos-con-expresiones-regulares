class NodoAST:
    # Clase para todos los nodos de AST
    pass

    def traducirPy(self):
        #Traducción de C++ a Python
        raise NotImplementedError('Metodo traducirPy() no implementado en este Nodo')
        

    def generarCodigo():
        #Traducir de C++ a Assembler
        raise NotImplementedError('Metodo generarCodigo() no implementado en este Nodo')

class NodoPrograma(NodoAST):
    # Nodo que representa a un programa completo
    def __init__(self, funciones, main):
        self.variables = []
        self.funciones = funciones
        self.main = main

class NodoLlamadaFuncion(NodoAST):
    # Nodo que representa una llamada a función
    def __init__(self, nombref, argumentos):
        self.nombre_funcion = nombref
        self.argumentos = argumentos

class NodoFuncion(NodoAST):
    # Nodo que representa la funcion
    def __init__(self, tipo, nombre, parametros, cuerpo):
        self.tipo = tipo
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo

    def traducirPy(self):
        params = ', '.join(p.traducirPy() for p in self.parametros)
        cuerpo = "\n    ".join(c.traducirPy() for c in self.cuerpo)
        return f"def {self.nombre[1]}({params}):\n    {cuerpo}"
        

class NodoParametros(NodoAST):
    # Nodo que representa a un parametro de funcion
    def __init__(self, tipo, nombre):
        self.tipo = tipo
        self.nombre = nombre

    def traducirPy(self):
        return self.nombre[1]

class NodoAsignacion(NodoAST):
    # Nodo que representa un asignacion de variables
    def __init__(self, tipo, nombre, expresion):
        self.tipo = tipo
        self.nombre = nombre
        self.expresion = expresion

    def traducirPy(self):
        return f'{self.nombre[1]} = {self.expresion.traducirPy()}'

class NodoOperacion(NodoAST):
    # Nodo que representa una operacion aritmetica
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

    def traducirPy(self):
        return f'{self.izquierda.traducirPy()} {self.operador[1]} {self.derecha.traducirPy()}'

        

class NodoRetorno(NodoAST):
    # Nodo que representa a la sentencia return
    def __init__(self, expresion):
        self.expresion = expresion

    def traducirPy(self):
        return f'return {self.expresion.traducirPy()}'

class NodoIdentificador(NodoAST):
    # Nodo que representa a un identificador
    def __init__(self, nombre):
        self.nombre = nombre

    def traducirPy(self):
        return self.nombre[1]

class NodoNumero(NodoAST):
    # Nodo que representa a un numero
    def __init__(self,valor):
        self.valor = valor

    def traducirPy(self):
        return str(self.valor[1])

class NodoImpresion(NodoAST):
    def __init__(self, texto):
        self.texto = texto
       

    def traducirPy(self):
        return f'print({self.texto[1]})'
        
    
    

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
        # Punto de entrada: se espera una funcion
        return self.funcion()

    def funcion(self):
        # Gramatica para una funcion: int IDENTIFIER (int IDENTIFIER) {cuerpo}
        tipo_retorno = self.coincidir('KEYWORD') # Tipo de retorno (ej. int)
        nombre_funcion = self.coincidir('IDENTIFIER') # Nombre de la funcion
        self.coincidir('DELIMITER') # Se espera un (
        if nombre_funcion[1] == 'main':
            parametros = []
        else:
            parametros = self.parametros() # Regla para los parametros
        self.coincidir('DELIMITER') # Se espera un )
        self.coincidir('DELIMITER') # Se espera un {
        cuerpo = self.cuerpo() # Regla parael cuerpo de la funcino
        self.coincidir('DELIMITER') # Se espera un }
        return NodoFuncion(tipo_retorno, nombre_funcion, parametros, cuerpo)

    def parametros(self):
        lista_parametros = []
        # Reglas para parametros: int IDENTIFIER (, int IDENTIFIER)*
        tipo = self.coincidir('KEYWORD') # Tipo de parametro
        nombre = self.coincidir('IDENTIFIER') # Nombre del parametro
        lista_parametros.append(NodoParametros(tipo, nombre))
        while self.obtener_token_actual() and self.obtener_token_actual()[1] == ',': 
            self.coincidir('DELIMITER') # Se espera una ,
            tipo = self.coincidir('KEYWORD') # Tipo de parametro
            nombre = self.coincidir('IDENTIFIER') # Nombre del parametro
            lista_parametros.append(NodoParametros(tipo, nombre))
        return lista_parametros

    def cuerpo(self):
        # Gramatica para el cuerpo: return IDENTIFIER OPERATOR IDENTIFIER:
        instrucciones = []
        while self.obtener_token_actual() and self.obtener_token_actual()[1] != '}':
            if self.obtener_token_actual()[1] == 'return':
                instrucciones.append(self.retorno())

            elif self.obtener_token_actual()[1] == 'print':
                instrucciones.append(self.impresion())
                
            else:
                instrucciones.append(self.asignacion())
        return instrucciones

    def asignacion(self):
        #Gramatica para la estructura de una asignación
        tipo = self.coincidir('KEYWORD') #Se espera un tipo
        nombre = self.coincidir('IDENTIFIER')
        self.coincidir('OPERATOR') # Se espera un =
        expresion = self.expresion()
        self.coincidir('DELIMITER') #Se espera un ;
        return NodoAsignacion(tipo, nombre, expresion)

    def retorno(self):
        self.coincidir('KEYWORD') #Se espera un return
        expresion = self.expresion()
        self.coincidir('DELIMITER') #Se espera un ;
        return NodoRetorno(expresion)

    def expresion(self):
        izquierda = self.termino()
        while self.obtener_token_actual() and self.obtener_token_actual()[0] == 'OPERATOR':
            operador = self.coincidir('OPERATOR')
            derecha = self.termino()
            izquierda = NodoOperacion(izquierda, operador, derecha)
        return izquierda

    def termino(self):
        token = self.obtener_token_actual()
        if token[0] == 'NUMBER':
            return NodoNumero(self.coincidir('NUMBER'))

        elif token[0] == 'IDENTIFIER':
            identificador = self.coincidir('IDENTIFIER')
            if self.obtener_token_actual() and self.obtener_token_actual()[1] == '(':
                self.coincidir('DELIMITER')
                argumentos = self.llamadaFuncion()
                self.coincidir('DELIMITER')
                return NodoLlamadaFuncion(identificador[1], argumentos)

            else:
                return NodoIdentificador(identificador)
        else:
            raise SyntaxError(f'Expresion no válida: {token}')


    def llamadaFuncion(self):
        argumentos = []
        # Reglas para Argumentos: IDENTIFIERE | NUMBER (, IDENTIFIER | NUMBER)*
        sigue = True
        token = self.obtener_token_actual()
        while sigue:
            sigue = False
            if token[0] == 'NUMBER':
                argumento = NodoNumero(self.coincidir('NUMBER'))

            elif token[0] == 'IDENTIFIER':
                argumento = NodoIdentificador(self.coincidir('IDENTIFIER'))
            else:
                raise SyntaxError(f'Error de Sintaxis, Se Esperaba un IDENTIFICADOR|Numero pero se encontró {token}')
            argumentos.append(argumento)

            if self.obtener_token_actual() and self.obtener_token_actual()[1] == ',':
                self.coincidir('DELIMITER') # Se espera una coma
                token = self.obtener_token_actual()
                sigue = True

        return argumentos

    def impresion(self):
        token_print = self.coincidir('KEYWORD')
        self.coincidir('DELIMITER')
        
        token_actual = self.obtener_token_actual()
        
        if token_actual[0] == 'STRING':
            contenido = self.coincidir('STRING')
        else:
            contenido = self.expresion()
            
        self.coincidir('DELIMITER')
        self.coincidir('DELIMITER')
        return NodoImpresion(contenido)


                    
                
            
        


        

            

    
        

  

        
