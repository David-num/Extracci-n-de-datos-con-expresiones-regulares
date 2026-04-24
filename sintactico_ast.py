class NodoAST:
    # Clase para todos los nodos de AST
    pass

    def traducirPy(self):
        # Traduccion de C++ a Python
        raise NotImplementedError('Metodo traducirPy() no implementado en este Nodo.')

    def traducirRuby(self):
        # Traduccion de C++ a Python
        raise NotImplementedError('Metodo traducirRuby() no implementado en este Nodo.')

    def generarCodigo():
        # Traducir de C++ ASSEMBLER
        raise NotImplementedError('Metodo generarCodigo() no implementado en este Nodo.')     

class NodoPrograma(NodoAST):
    # Nodo que representa un programa completo
    def __init__(self, funciones, main):
        self.variables = []
        self.funciones = funciones
        self.main = main

class NodoLlamadaFuncion(NodoAST):
    # Nodo que representa una llamada de funcion
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
        params = ", ".join(p.traducirPy() for p in self.parametros)
        cuerpo = "\n    ".join(c.traducirPy() for c in self.cuerpo)
        return f"def {self.nombre[1]}({params}):\n    {cuerpo}"

    def traducirRuby(self):
        params = ", ".join(p.traducirRuby() for p in self.parametros)
        cuerpo = "\n  ".join(c.traducirRuby() for c in self.cuerpo)
        return f"def {self.nombre[1]}({params})\n  {cuerpo}\nend"

class NodoParametro(NodoAST):
    # Nodo que representa a un parametro de funcion
    def __init__(self, tipo, nombre):
        self.tipo = tipo
        self.nombre = nombre

    def traducirPy(self):
        return self.nombre[1]

    def traducirRuby(self):
        return self.nombre[1]

class NodoAsignacion(NodoAST):
    # Nodo que representa un asignacion de variables
    def __init__(self, tipo, nombre, expresion):
        self.tipo = tipo
        self.nombre = nombre
        self.expresion = expresion

    def traducirPy(self):
        return f'{self.nombre[1]} = {self.expresion.traducirPy()}'

    def traducirRuby(self):
        return f'{self.nombre[1]} = {self.expresion.traducirRuby()}'

class NodoOperacion(NodoAST):
    # Nodo que representa una operacion aritmetica
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

    def traducirPy(self):
        return f'{self.izquierda.traducirPy()} {self.operador[1]} {self.derecha.traducirPy()}'

    def traducirRuby(self):
        return f'{self.izquierda.traducirRuby()} {self.operador[1]} {self.derecha.traducirRuby()}'

class NodoRetorno(NodoAST):
    # Nodo que representa a la sentencia return
    def __init__(self, expresion):
        self.expresion = expresion

    def traducirPy(self):
        return f'return {self.expresion.traducirPy()}'

    def traducirRuby(self):
        return f'return {self.expresion.traducirRuby()}'

class NodoIdentificador(NodoAST):
    # Nodo que representa a un identificador
    def __init__(self, nombre):
        self.nombre = nombre

    def traducirPy(self):
        return self.nombre[1]

    def traducirRuby(self):
        return self.nombre[1]

class NodoNumero(NodoAST):
    # Nodo que representa a un numero
    def __init__(self,valor):
        self.valor = valor

    def traducirPy(self):
        return str(self.valor[1])

    def traducirRuby(self):
        return str(self.valor[1])

class NodoCadena(NodoAST):
    # Nodo que representa a una cadena
    def __init__(self, valor):
        self.valor = valor 

    def traducirPy(self):
        return self.valor[1] 

    def traducirRuby(self):
        return self.valor[1]

class NodoPrint(NodoAST):
    # Nodo que representa la sentencia print
    def __init__(self, argumentos):
        self.argumentos = argumentos

    def traducirPy(self):
        args = ", ".join(a.traducirPy() for a in self.argumentos)
        return f"print({args})"

    def traducirRuby(self):
        args = ", ".join(a.traducirRuby() for a in self.argumentos)
        return f"puts({args})"

class NodoPrintf(NodoAST):
    def __init__(self, argumentos):
        self.argumentos = argumentos 

    def traducirPy(self):
        # Caso vacío
        if not self.argumentos:
            return "print()"

        formato = self.argumentos[0]
        vars_ = self.argumentos[1:]

        # Si el primer argumento NO es string, caemos a print normal
        if not isinstance(formato, NodoCadena):
            args = ", ".join(a.traducirPy() for a in self.argumentos)
            return f"print({args})"

        # formato.valor[1] incluye comillas -> '"Hola %d"'
        texto_con_comillas = formato.valor[1]
        contenido = texto_con_comillas[1:-1]  # sin comillas

        # Reemplazo básico: %d %f %s -> {variable}
        for v in vars_:
            if "%d" in contenido:
                contenido = contenido.replace("%d", "{" + v.traducirPy() + "}", 1)
            elif "%f" in contenido:
                contenido = contenido.replace("%f", "{" + v.traducirPy() + "}", 1)
            elif "%s" in contenido:
                contenido = contenido.replace("%s", "{" + v.traducirPy() + "}", 1)

        return f'print(f"{contenido}")'

    def traducirRuby(self):
        args = ", ".join(a.traducirRuby() for a in self.argumentos)
        return f"printf({args})"


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
        lista_parametros.append(NodoParametro(tipo, nombre))
        while self.obtener_token_actual() and self.obtener_token_actual()[1] == ',': 
            self.coincidir('DELIMITER') # Se espera una ,
            tipo = self.coincidir('KEYWORD') # Tipo de parametro
            nombre = self.coincidir('IDENTIFIER') # Nombre del parametro
            lista_parametros.append(NodoParametro(tipo, nombre))
        return lista_parametros

    def cuerpo(self):
        # Gramatica para el cuerpo: return IDENTIFIER OPERATOR IDENTIFIER:
        instrucciones = []
        while self.obtener_token_actual() and self.obtener_token_actual()[1] != '}': 
            if self.obtener_token_actual()[1] == 'return':
                instrucciones.append(self.retorno())
            elif self.obtener_token_actual()[1] == 'print':
                instrucciones.append(self.sentencia_print())
            elif self.obtener_token_actual()[1] == 'printf':
                instrucciones.append(self.sentencia_printf())
            else:
                instrucciones.append(self.asignacion())
        return instrucciones

    def asignacion(self):
        # Gramatica para la estructura de una asignacion
        tipo = self.coincidir('KEYWORD') # Se espera un tipo
        nombre = self.coincidir('IDENTIFIER')
        self.coincidir('OPERATOR') # Se espera un =
        expresion = self.expresion() 
        self.coincidir('DELIMITER') # Se espera un ;
        return NodoAsignacion(tipo, nombre, expresion)

    def retorno(self):
        self.coincidir('KEYWORD') # Se espera un return
        expresion = self.expresion()
        self.coincidir('DELIMITER') # Se espera un ;
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
        elif token[0] == 'STRING':
            return NodoCadena(self.coincidir('STRING'))
        else:
            raise SyntaxError(f'Expresion no valida: {token}')

    def llamadaFuncion(self):
        argumentos = []
        # Reglas para argumentos: IDENTIFIER | NUMBER (, IDENTIFIER | NUMBER)*
        sigue = True
        token = self.obtener_token_actual()
        while sigue:
            sigue = False
            if token[0] == 'NUMBER':
                argumento = NodoNumero(self.coincidir('NUMBER'))
            elif token[0] == 'IDENTIFIER':
                argumento = NodoIdentificador(self.coincidir('IDENTIFIER'))
            elif token[0] == 'STRING':
                argumento = NodoCadena(self.coincidir('STRING'))
            else:
                raise SyntaxError(f'Error de sintaxis, se esperaba un IDENTsIFICADOR|NUMERO pero se encontro_ {token}')
            argumentos.append(argumento)
            if self.obtener_token_actual() and self.obtener_token_actual()[1] == ',':
                self.coincidir('DELIMITER') # Se espera una coma
                token = self.obtener_token_actual()
                sigue = True
        return argumentos

    def sentencia_print(self):
        self.coincidir('KEYWORD')     
        self.coincidir('DELIMITER')   
        argumentos = []
        if self.obtener_token_actual() and self.obtener_token_actual()[1] != ')':
            argumentos = self.llamadaFuncion()
        self.coincidir('DELIMITER')  
        self.coincidir('DELIMITER')   
        return NodoPrint(argumentos)    
    
    def sentencia_printf(self):
        self.coincidir('KEYWORD')    
        self.coincidir('DELIMITER')   
        argumentos = []
        if self.obtener_token_actual() and self.obtener_token_actual()[1] != ')':
            argumentos = self.llamadaFuncion()
        self.coincidir('DELIMITER')   
        self.coincidir('DELIMITER')   
        return NodoPrintf(argumentos)
