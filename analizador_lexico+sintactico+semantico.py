# ANALIZADOR LÉXICO + SINTÁCTICO


# ================================================================================
# ANALIZADOR LÉXICO
# ================================================================================
# Función: Convierte el código fuente en una secuencia de tokens
# Reconoce: Palabras reservadas, identificadores, números, operadores y símbolos
# ================================================================================

#FUNCIONES AUXILIARES 
def es_letra(c):
    """Verifica si un carácter es una letra (a-z, A-Z)"""
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')

def es_digito(c):
    """Verifica si un carácter es un dígito (0-9)"""
    return '0' <= c <= '9'

def analizar(codigo):
    """
    Analizador léxico principal
    Retorna: (tokens)
    - tokens: Lista de códigos numéricos de tokens
    - lineas: Lista de números de línea donde aparece cada token
    - lexemas: Lista de cadenas originales del código fuente
    """
    tokens = []
    lineas = []
    lexemas = []
    i = 0
    linea = 1
    col = 1
    n = len(codigo)

    while i < n:
        c = codigo[i]
        col_inicio = col

        # ----------------------------------------------------------------
        # ESPACIOS EN BLANCO (no generan tokens)
        # ----------------------------------------------------------------
        if c.isspace():
            if c == "\n":
                linea += 1
                col = 1
            else:
                col += 1
            i += 1
            continue

        # ----------------------------------------------------------------
        # OPERADORES DOBLES (deben verificarse ANTES de los simples)
        # Token 120: ==  (igualdad)
        # Token 121: !=  (diferente)
        # Token 123: <=  (menor o igual)
        # Token 125: >=  (mayor o igual)
        # ----------------------------------------------------------------
        if i + 1 < n:
            d = codigo[i+1]

            if c == "=" and d == "=":
                tokens.append(120)  # Token 120: ==
                lineas.append(linea)
                lexemas.append("==")
                i += 2
                col += 2
                continue

            if c == "!" and d == "=":
                tokens.append(121)  # Token 121: !=
                lineas.append(linea)
                lexemas.append("!=")
                i += 2
                col += 2
                continue

            if c == "<" and d == "=":
                tokens.append(123)  # Token 123: <=
                lineas.append(linea)
                lexemas.append("<=")
                i += 2
                col += 2
                continue

            if c == ">" and d == "=":
                tokens.append(125)  # Token 125: >=
                lineas.append(linea)
                lexemas.append(">=")
                i += 2
                col += 2
                continue

        # ----------------------------------------------------------------
        # SÍMBOLOS SIMPLES
        # Token 100: =   (asignación)
        # Token 101: (   (paréntesis izquierdo)
        # Token 102: )   (paréntesis derecho)
        # Token 103: -   (resta o menos unario)
        # Token 104: +   (suma)
        # Token 105: ;   (punto y coma)
        # Token 106: *   (multiplicación)
        # Token 107: /   (división)
        # Token 108: ,   (coma)
        # Token 122: <   (menor que)
        # Token 124: >   (mayor que)
        # ----------------------------------------------------------------
        if c == "=":
            tokens.append(100)  # Token 100: =
            lineas.append(linea)
            lexemas.append("=")
            i += 1
            col += 1
            continue
        elif c == "(":
            tokens.append(101)  # Token 101: (
            lineas.append(linea)
            lexemas.append("(")
            i += 1
            col += 1
            continue
        elif c == ")":
            tokens.append(102)  # Token 102: )
            lineas.append(linea)
            lexemas.append(")")
            i += 1
            col += 1
            continue
        elif c == "-":
            tokens.append(103)  # Token 103: -
            lineas.append(linea)
            lexemas.append("-")
            i += 1
            col += 1
            continue
        elif c == "+":
            tokens.append(104)  # Token 104: +
            lineas.append(linea)
            lexemas.append("+")
            i += 1
            col += 1
            continue
        elif c == ";":
            tokens.append(105)  # Token 105: ;
            lineas.append(linea)
            lexemas.append(";")
            i += 1
            col += 1
            continue
        elif c == "*":
            tokens.append(106)  # Token 106: *
            lineas.append(linea)
            lexemas.append("*")
            i += 1
            col += 1
            continue
        elif c == "/":
            tokens.append(107)  # Token 107: /
            lineas.append(linea)
            lexemas.append("/")
            i += 1
            col += 1
            continue
        elif c == ",":
            tokens.append(108)  # Token 108: ,
            lineas.append(linea)
            lexemas.append(",")
            i += 1
            col += 1
            continue
        elif c == "<":
            tokens.append(122)  # Token 122: <
            lineas.append(linea)
            lexemas.append("<")
            i += 1
            col += 1
            continue
        elif c == ">":
            tokens.append(124)  # Token 124: >
            lineas.append(linea)
            lexemas.append(">")
            i += 1
            col += 1
            continue

        # ----------------------------------------------------------------
        # NÚMEROS (Token 700)
        # Reconoce: Secuencias de dígitos
        # Error: Si un número es seguido por letra o guion bajo
        # ----------------------------------------------------------------
        if es_digito(c):
            numero = ""
            
            while i < n and es_digito(codigo[i]):
                numero += codigo[i]
                i += 1
                col += 1
            
            # Verificar si continúa con letra o guion bajo (ERROR LÉXICO)
            if i < n and (es_letra(codigo[i]) or codigo[i] == '_'):
                lexema_error = numero
                while i < n and (es_letra(codigo[i]) or es_digito(codigo[i]) or codigo[i] == '_'):
                    lexema_error += codigo[i]
                    i += 1
                    col += 1
                
                print(f"Error léxico: símbolo '{lexema_error}' no reconocido (línea {linea}, columna {col_inicio})")
                tokens.append(900)  # Token 900: ERROR
                lineas.append(linea)
                lexemas.append(lexema_error)
                return tokens, lineas, lexemas
            
            tokens.append(700)  # Token 700: NUMERO
            lineas.append(linea)
            lexemas.append(numero)
            continue
        # ----------------------------------------------------------------
        # IDENTIFICADORES Y PALABRAS RESERVADAS
        # Identificadores (Token 500): Variables definidas por el usuario
        # Palabras Reservadas (Tokens 1-19): Palabras clave del lenguaje
        # ----------------------------------------------------------------
        if es_letra(c):
            lexema = ""
            
            lexema += c
            i += 1
            col += 1
            
            # Capturar secuencia completa: letras, dígitos y guiones bajos
            while i < n and (es_letra(codigo[i]) or es_digito(codigo[i]) or codigo[i] == "_"):
                lexema += codigo[i]
                i += 1
                col += 1
          
            # ----------------------------------------------------------------
            # PALABRAS RESERVADAS (Tokens 1-19)
            # Token 1: inicio
            # Token 2: fin
            # Token 3: entero
            # Token 4: imprimir
            # Token 5: ingresa
            # Token 6: si
            # Token 7: entonces
            # Token 8: sino
            # Token 9: fin_si
            # Token 10: mientras_que
            # Token 11: hacer
            # Token 12: fin_mientras_que
            # Token 13: repetir
            # Token 14: hasta_que
            # Token 15: para
            # Token 16: fin_para
            # Token 17: no
            # Token 18: y
            # Token 19: o
            # Token 500: IDENTIFICADOR (si no coincide con ninguna palabra reservada)
            # ----------------------------------------------------------------
            if lexema == "inicio":
                tokens.append(1)
            elif lexema == "fin":
                tokens.append(2)
            elif lexema == "entero":
                tokens.append(3)
            elif lexema == "imprimir":
                tokens.append(4)
            elif lexema == "ingresa":
                tokens.append(5)
            elif lexema == "si":
                tokens.append(6)
            elif lexema == "entonces":
                tokens.append(7)
            elif lexema == "sino":
                tokens.append(8)
            elif lexema == "fin_si":
                tokens.append(9)
            elif lexema == "mientras_que":
                tokens.append(10)
            elif lexema == "hacer":
                tokens.append(11)
            elif lexema == "fin_mientras_que":
                tokens.append(12)
            elif lexema == "repetir":
                tokens.append(13)
            elif lexema == "hasta_que":
                tokens.append(14)
            elif lexema == "para":
                tokens.append(15)
            elif lexema == "fin_para":
                tokens.append(16)
            elif lexema == "no":
                tokens.append(17)
            elif lexema == "y":
                tokens.append(18)
            elif lexema == "o":
                tokens.append(19)
            else:
                tokens.append(500)  # Token 500: IDENTIFICADOR

            lineas.append(linea)
            lexemas.append(lexema)
            continue

        # ----------------------------------------------------------------
        # ERROR - CARACTER NO RECONOCIDO (Token 900)
        # ----------------------------------------------------------------
        print(f"Error léxico: símbolo '{c}' no reconocido (línea {linea})")
        tokens.append(900)  # Token 900: ERROR
        lineas.append(linea)
        lexemas.append(c)
        return tokens, lineas, lexemas

    return tokens, lineas, lexemas
    

# ================================================================================
# ANALIZADOR SINTÁCTICO
# ================================================================================
# Función: Verifica que la secuencia de tokens cumpla con la gramática
# Método: Análisis descendente recursivo (Recursive Descent Parser)
# Cada función representa una regla de producción de la gramática EBNF
# ================================================================================

# Variables globales del analizador sintáctico
tokens = []
lineas = []
lexemas = []
posicion = 0
token_actual = None
linea_actual = None
lexema_actual = None
hay_error = False

def avanzar():
    """Avanza al siguiente token en la lista"""
    global posicion, token_actual, linea_actual, lexema_actual
    posicion += 1
    if posicion < len(tokens):
        token_actual = tokens[posicion]
        linea_actual = lineas[posicion]
        lexema_actual = lexemas[posicion]
    else:
        token_actual = None
        linea_actual = None
        lexema_actual = None

def simbolo(tok):
    """Convierte código de token a nombre legible para mensajes de error"""
    if tok is None:
        return "fin de archivo"
    if tok == 1: return "inicio"
    elif tok == 2: return "fin"
    elif tok == 3: return "entero"
    elif tok == 4: return "imprimir"
    elif tok == 5: return "ingresa"
    elif tok == 6: return "si"
    elif tok == 7: return "entonces"
    elif tok == 8: return "sino"
    elif tok == 9: return "fin_si"
    elif tok == 10: return "mientras_que"
    elif tok == 11: return "hacer"
    elif tok == 12: return "fin_mientras_que"
    elif tok == 13: return "repetir"
    elif tok == 14: return "hasta_que"
    elif tok == 15: return "para"
    elif tok == 16: return "fin_para"
    elif tok == 17: return "no"
    elif tok == 18: return "y"
    elif tok == 19: return "o"
    elif tok == 100: return "="
    elif tok == 101: return "("
    elif tok == 102: return ")"
    elif tok == 103: return "-"
    elif tok == 104: return "+"
    elif tok == 105: return ";"
    elif tok == 106: return "*"
    elif tok == 107: return "/"
    elif tok == 108: return ","
    elif tok == 120: return "=="
    elif tok == 121: return "!="
    elif tok == 122: return "<"
    elif tok == 123: return "<="
    elif tok == 124: return ">"
    elif tok == 125: return ">="
    elif tok == 500: return "identificador"
    elif tok == 700: return "numero"
    elif tok == 900: return "error"
    else: return str(tok)

def error(mensaje):
    """Reporta un error sintáctico y termina el análisis"""
    global hay_error
    hay_error = True
    if token_actual is None:
        print(f"Error de sintaxis: {mensaje}. Token actual: fin de archivo")
    else:
        print(f"Error de sintaxis en la linea {linea_actual}: se encontro '{lexema_actual}' pero se esperaba {mensaje}")
    exit()

def coincidir(esperado):
    """Verifica que el token actual coincida con el esperado y avanza"""
    global token_actual
    if token_actual == esperado:
        avanzar()
    else:
        error(f"'{simbolo(esperado)}'")

# ================================================================================
# FUNCIONES DE LA GRAMÁTICA
# ================================================================================

def programa():
    """
    Gramática: programa = "inicio", { declaracion }, { sentencia }, "fin" ;
    Representa la estructura principal del programa
    """
    # Verificar que comience con "inicio"
    if token_actual != 1:
        if token_actual == 500 and lexema_actual.lower() == "inicio":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(1)  # Token 1: inicio
    
    # Procesar todas las declaraciones (entero ...)
    while token_actual is not None and token_actual == 3:
        declaracion()
    
    # Verificar error común: usar "Entero" en lugar de "entero"
    if token_actual == 500 and lexema_actual.lower() == "entero":
        error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    
    # Procesar todas las sentencias (asignaciones, imprimir, si, mientras, etc.)
    while token_actual is not None and token_actual in [4, 5, 6, 10, 13, 15, 500]:
        sentencia()
    
    # Verificar que termine con "fin"
    if token_actual != 2:
        if token_actual == 500 and lexema_actual.lower() == "fin":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(2)  # Token 2: fin

def declaracion():
    """
    Gramática: declaracion = "entero", lista_decl, ";" ;
    Declara variables de tipo entero
    """
    if token_actual != 3:
        if token_actual == 500 and lexema_actual.lower() == "entero":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(3)  # Token 3: entero
    lista_decl()
    coincidir(105)  # Token 105: ;

def lista_decl():
    """
    Gramática: lista_decl = identificador, [ "=", expresion ],
                            { ",", identificador, [ "=", expresion ] } ;
    Lista de variables con inicialización opcional
    Ejemplos: x; o x = 5; o x, y = 3, z;
    """
    coincidir(500)  # Token 500: identificador
    
    # Inicialización opcional de la primera variable
    if token_actual is not None and token_actual == 100:
        coincidir(100)  # Token 100: =
        expresion()
    
    # Variables adicionales separadas por comas
    while token_actual is not None and token_actual == 108:
        coincidir(108)  # Token 108: ,
        coincidir(500)  # Token 500: identificador
        
        # Inicialización opcional de variables adicionales
        if token_actual is not None and token_actual == 100:
            coincidir(100)  # Token 100: =
            expresion()

def sentencia():
    """
    Gramática: sentencia = asignacion | imprimir | ingresa | si | mientras | repetir | para ;
    Representa cualquier sentencia ejecutable del programa
    """
    if token_actual is None:
        error("una sentencia valida")
    
    # Determinar qué tipo de sentencia es según el token actual
    if token_actual == 4:
        imprimir()
    elif token_actual == 5:
        ingresa()
    elif token_actual == 6:
        si()
    elif token_actual == 10:
        mientras()
    elif token_actual == 13:
        repetir()
    elif token_actual == 15:
        para()
    elif token_actual == 500:
        # Verificar que no sea una palabra reservada mal escrita
        if lexema_actual.lower() in ["imprimir", "ingresa", "si", "entonces", "sino", "mientras_que", "hacer", "repetir", "hasta_que", "para", "entero", "inicio", "fin", "fin_si", "fin_mientras_que", "fin_para", "no", "y", "o"]:
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
        asignacion()
    else:
        error("una sentencia valida")

def asignacion():
    """
    Gramática: asignacion = identificador, "=", expresion, ";" ;
    Asigna el valor de una expresión a una variable
    Ejemplo: x = 5 + 3;
    """
    coincidir(500)  # Token 500: identificador
    coincidir(100)  # Token 100: =
    expresion()
    coincidir(105)  # Token 105: ;

def imprimir():
    """
    Gramática: imprimir = "imprimir", "(", expresion, { ",", expresion }, ")", ";" ;
    Imprime una o más expresiones
    Ejemplo: imprimir(x, y + 2);
    """
    if token_actual != 4:
        if token_actual == 500 and lexema_actual.lower() == "imprimir":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(4)    # Token 4: imprimir
    coincidir(101)  # Token 101: (
    expresion()
    
    # Expresiones adicionales separadas por comas
    while token_actual is not None and token_actual == 108:
        coincidir(108)  # Token 108: ,
        expresion()
    
    coincidir(102)  # Token 102: )
    coincidir(105)  # Token 105: ;

def ingresa():
    """
    Gramática: ingresa = "ingresa", "(", identificador, ")", ";" ;
    Lee un valor desde la entrada y lo almacena en una variable
    Ejemplo: ingresa(x);
    """
    if token_actual != 5:
        if token_actual == 500 and lexema_actual.lower() == "ingresa":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(5)    # Token 5: ingresa
    coincidir(101)  # Token 101: (
    coincidir(500)  # Token 500: identificador
    coincidir(102)  # Token 102: )
    coincidir(105)  # Token 105: ;

def si():
    """
    Gramática: si = "si", "(", condicion, ")", "entonces", bloque,
                    [ "sino", bloque ], "fin_si", ";" ;
    Estructura condicional if-then-else
    Ejemplo: si (x > 0) entonces ... sino ... fin_si;
    """
    if token_actual != 6:
        if token_actual == 500 and lexema_actual.lower() == "si":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(6)    # Token 6: si
    coincidir(101)  # Token 101: (
    condicion()
    coincidir(102)  # Token 102: )
    
    if token_actual != 7:
        if token_actual == 500 and lexema_actual.lower() == "entonces":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(7)    # Token 7: entonces
    bloque()
    
    # Parte "sino" opcional
    if token_actual is not None and token_actual == 8:
        coincidir(8)  # Token 8: sino
        bloque()
    elif token_actual == 500 and lexema_actual.lower() == "sino":
        error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    
    if token_actual != 9:
        if token_actual == 500 and lexema_actual.lower() == "fin_si":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(9)    # Token 9: fin_si
    coincidir(105)  # Token 105: ;

def mientras():
    """
    Gramática: mientras = "mientras_que", "(", condicion, ")",
                          "hacer", bloque, "fin_mientras_que", ";" ;
    Bucle while
    Ejemplo: mientras_que (x < 10) hacer ... fin_mientras_que;
    """
    if token_actual != 10:
        if token_actual == 500 and lexema_actual.lower() == "mientras_que":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(10)   # Token 10: mientras_que
    coincidir(101)  # Token 101: (
    condicion()
    coincidir(102)  # Token 102: )
    
    if token_actual != 11:
        if token_actual == 500 and lexema_actual.lower() == "hacer":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(11)   # Token 11: hacer
    bloque()
    
    if token_actual != 12:
        if token_actual == 500 and lexema_actual.lower() == "fin_mientras_que":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(12)   # Token 12: fin_mientras_que
    coincidir(105)  # Token 105: ;

def repetir():
    """
    Gramática: repetir = "repetir", bloque, "hasta_que", "(", condicion, ")", ";" ;
    Bucle do-while (se ejecuta al menos una vez)
    Ejemplo: repetir ... hasta_que (x > 10);
    """
    if token_actual != 13:
        if token_actual == 500 and lexema_actual.lower() == "repetir":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(13)   # Token 13: repetir
    bloque()
    
    if token_actual != 14:
        if token_actual == 500 and lexema_actual.lower() == "hasta_que":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(14)   # Token 14: hasta_que
    coincidir(101)  # Token 101: (
    condicion()
    coincidir(102)  # Token 102: )
    coincidir(105)  # Token 105: ;

def para():
    """
    Gramática: para = "para", "(", inicializacion, ";", condicion, ";", actualizacion, ")",
                      "hacer", bloque, "fin_para", ";" ;
    Bucle for con inicialización, condición y actualización
    Ejemplo: para(i = 0; i < 10; i = i + 1) hacer ... fin_para;
    """
    if token_actual != 15:
        if token_actual == 500 and lexema_actual.lower() == "para":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(15)   # Token 15: para
    coincidir(101)  # Token 101: (
    inicializacion()
    coincidir(105)  # Token 105: ;
    condicion()
    coincidir(105)  # Token 105: ;
    actualizacion()
    coincidir(102)  # Token 102: )
    
    if token_actual != 11:
        if token_actual == 500 and lexema_actual.lower() == "hacer":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(11)   # Token 11: hacer
    bloque()
    
    if token_actual != 16:
        if token_actual == 500 and lexema_actual.lower() == "fin_para":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(16)   # Token 16: fin_para
    coincidir(105)  # Token 105: ;

def inicializacion():
    """
    Gramática: inicializacion = [ "entero" ], identificador, "=", expresion ;
    Inicialización en bucle for (puede declarar variable nueva o usar existente)
    Ejemplos: i = 0  o  entero i = 0
    """
    # "entero" es opcional
    if token_actual is not None and token_actual == 3:
        coincidir(3)  # Token 3: entero
    elif token_actual == 500 and lexema_actual.lower() == "entero":
        error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    
    coincidir(500)  # Token 500: identificador
    coincidir(100)  # Token 100: =
    expresion()

def actualizacion():
    """
    Gramática: actualizacion = identificador, "=", expresion ;
    Actualización en bucle for
    Ejemplo: i = i + 1
    """
    coincidir(500)  # Token 500: identificador
    coincidir(100)  # Token 100: =
    expresion()

def bloque():
    """
    Gramática: bloque = { sentencia } ;
    Secuencia de cero o más sentencias
    """
    while token_actual is not None and token_actual in [4, 5, 6, 10, 13, 15, 500]:
        sentencia()

def condicion():
    """
    Gramática: condicion = condicion_simple, { operador_logico_binario, condicion_simple } ;
    Expresión booleana con operadores lógicos (y, o)
    Ejemplo: x > 0 y x < 10
    """
    condicion_simple()
    
    # Operadores lógicos: 18 = y (AND), 19 = o (OR)
    while token_actual is not None and token_actual in [18, 19]:
        avanzar()
        condicion_simple()

def condicion_simple():
    """
    Gramática: condicion_simple = expresion, operador_relacional, expresion
                                  | "no", condicion_simple ;
    Comparación entre dos expresiones o negación
    Ejemplos: x > 5  o  no (x == 0)
    """
    # Negación "no"
    if token_actual is not None and token_actual == 17:
        coincidir(17)  # Token 17: no
        condicion_simple()
    elif token_actual == 500 and lexema_actual.lower() == "no":
        error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    else:
        # Comparación: expresion operador_relacional expresion
        expresion()
        operador_relacional()
        expresion()

def operador_relacional():
    """
    Gramática: operador_relacional = "==" | "!=" | "<" | "<=" | ">" | ">=" ;
    Operadores de comparación
    Tokens: 120(==), 121(!=), 122(<), 123(<=), 124(>), 125(>=)
    """
    if token_actual is not None and token_actual in [120, 121, 122, 123, 124, 125]:
        avanzar()
    else:
        error("un operador relacional (==, !=, <, <=, >, >=)")

def expresion():
    """
    Gramática: expresion = termino, { ("+" | "-"), termino } ;
    Expresión aritmética con suma y resta (menor precedencia)
    Ejemplo: a + b - c
    """
    termino()
    
    # Operadores de suma/resta: 104 = +, 103 = -
    while token_actual is not None and token_actual in [104, 103]:
        avanzar()
        termino()

def termino():
    """
    Gramática: termino = factor, { ("*" | "/"), factor } ;
    Término con multiplicación y división (mayor precedencia que +/-)
    Ejemplo: a * b / c
    """
    factor()
    
    # Operadores de multiplicación/división: 106 = *, 107 = /
    while token_actual is not None and token_actual in [106, 107]:
        avanzar()
        factor()


def factor():
    if token_actual is None:
        error("un factor (identificador, numero, o expresion entre parentesis)")
    
    if token_actual == 500:
        if lexema_actual.lower() in ["no"]:
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
        coincidir(500)
    elif token_actual == 700:
        coincidir(700)
    elif token_actual == 101:
        coincidir(101)
        expresion()
        coincidir(102)
    elif token_actual == 17:
        coincidir(17)
        factor()
    elif token_actual == 103:
        coincidir(103)
        factor()
    else:
        error("un factor (identificador, numero, o expresion entre parentesis)")

def analizar_sintactico(lista_tokens, lista_lineas, lista_lexemas):
    global tokens, lineas, lexemas, posicion, token_actual, linea_actual, lexema_actual, hay_error
    tokens = lista_tokens
    lineas = lista_lineas
    lexemas = lista_lexemas
    posicion = 0
    hay_error = False
    
    if len(tokens) == 0:
        print("Error: no hay tokens para analizar")
        hay_error = True
        return False
    
    token_actual = tokens[posicion]
    linea_actual = lineas[posicion]
    lexema_actual = lexemas[posicion]
    
    try:
        programa()
        
        if token_actual is not None:
            error("fin de programa, no se esperaban mas tokens")
        
        print("El codigo es sintacticamente correcto")
        return True
    except SystemExit:
        return False
    

# ----------------------------------------------
# CASOS DE PRUEBA
# ----------------------------------------------

# ======================================================================
print("\nCASO 1: Identificadores válidos")
print("\n" + "=" * 70)

codigo1 = """inicio
entero var_1, Var_2, num;
fin"""

tokens1, lineas1, lexemas1 = analizar(codigo1)
print("Tokens:", tokens1)
analizar_sintactico(tokens1, lineas1, lexemas1)


# ======================================================================
print("\n" + "=" * 70)
print("CASO 2: Programa válido")

codigo2 = """inicio
entero a, b, suma;
a = 10;
b = 20;
suma = a + b;
imprimir(suma);
fin"""

tokens2, lineas2, lexemas2 = analizar(codigo2)
print("Tokens:", tokens2)
analizar_sintactico(tokens2, lineas2, lexemas2)


# ======================================================================
print("\n" + "=" * 70)
print("\nCASO 3: ERROR - símbolo '@'")

codigo3 = """inicio
entero a;
a = 10 @ 20;
fin"""

tokens3, lineas3, lexemas3 = analizar(codigo3)
print("Tokens:", tokens3)
analizar_sintactico(tokens3, lineas3, lexemas3)


# ======================================================================
print("\n" + "=" * 70)
print("\nCASO 4: Ejemplo completo con ciclo para")

codigo4 = """inicio
entero a;
a = 10;
para(entero i = 0; i < 5; i = i + 1) hacer
    imprimir(i);
fin_para;
fin"""
tokens4, lineas4, lexemas4 = analizar(codigo4)
print("Tokens:", tokens4)
analizar_sintactico(tokens4, lineas4, lexemas4)


# ======================================================================
print("\n" + "=" * 70)
print("\nCASO 5: ERROR - numero con letras")

codigo5 = """inicio
entero a;
a = 1234ee33;
fin"""
print(analizar(codigo5))

tokens5, lineas5, lexemas5 = analizar(codigo5)
print("Tokens:", tokens5)
analizar_sintactico(tokens5, lineas5, lexemas5)


# ======================================================================
print("\n" + "=" * 70)
print("\nCASO 6: Condición SI")

codigo6 = """inicio
entero a;
a = 15;
si a > 10 entonces
    imprimir(a);
fin_si
fin"""

tokens6, lineas6, lexemas6 = analizar(codigo6)
print("Tokens:", tokens6)
analizar_sintactico(tokens6, lineas6, lexemas6)


# ======================================================================
print("\n" + "=" * 70)
print("\nCASO 7: Ciclo MIENTRAS")

codigo7 = """inicio
entero i;
i = 0;
mientras_que i < 5 hacer
    imprimir(i);
    i = i + 1;
fin_mientras_que
fin"""

tokens7, lineas7, lexemas7 = analizar(codigo7)
print("Tokens:", tokens7)
analizar_sintactico(tokens7, lineas7, lexemas7)


# ======================================================================
print("\n" + "=" * 70)
print("\nCASO 8: Ciclo REPETIR")

codigo8 = """inicio
entero x;
x = 1;
repetir
    imprimir(x);
    x = x + 1;
hasta_que x == 5;
fin"""

tokens8, lineas8, lexemas8 = analizar(codigo8)
print("Tokens:", tokens8)
analizar_sintactico(tokens8, lineas8, lexemas8)


# ======================================================================
print("\n" + "=" * 70)
print("\nCASO 9: Operadores relacionales")

codigo9 = """inicio
entero a, b;
a = 10;
b = 20;
si a != b entonces
    imprimir(a);
fin_si
si a <= b entonces
    imprimir(b);
fin_si
si b >= a entonces
    imprimir(a);
fin_si
fin"""

tokens9, lineas9, lexemas9 = analizar(codigo9)
print("Tokens:", tokens9)
analizar_sintactico(tokens9, lineas9, lexemas9)


# ======================================================================
print("\n" + "=" * 70)
print("\nCASO 10: ERROR - carácter '$'")

codigo10 = """inicio
entero total;
total = 50 $ 10;
fin"""
print(analizar(codigo10))

tokens10, lineas10, lexemas10 = analizar(codigo10)
print("Tokens:", tokens10)
analizar_sintactico(tokens10, lineas10, lexemas10)