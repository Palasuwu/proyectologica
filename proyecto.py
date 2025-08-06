import ply.lex as lex
import ply.yacc as yacc
from graphviz import Digraph

# Definicion de tokens y expresiones regulares
tokens = (
    'VAR', 'CONST', 'NOT', 'AND', 'OR', 'IMPLIES', 'BICOND', 'LPAREN', 'RPAREN'
)

# Mapeo de tokens a sus expresiones regulares
regex_map = {
    'VAR': r'[p-z]',       # Variables proposicionales
    'CONST': r'[01]',      # Constantes (0 y 1)
    'NOT': r'~',           # Operador de negacion
    'AND': r'\^',          # Operador AND
    'OR': r'o',            # Operador OR
    'IMPLIES': r'=>',      # Operador implica
    'BICOND': r'<=>',      # Operador bicondicional
    'LPAREN': r'\(',       # Parentesis izquierdo
    'RPAREN': r'\)'        # Parentesis derecho
}

# Asignacion de expresiones regulares a los tokens
t_VAR = regex_map['VAR']
t_CONST = regex_map['CONST']
t_NOT = regex_map['NOT']
t_AND = regex_map['AND']
t_OR = regex_map['OR']
t_IMPLIES = regex_map['IMPLIES']
t_BICOND = regex_map['BICOND']
t_LPAREN = regex_map['LPAREN']
t_RPAREN = regex_map['RPAREN']

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores lexicos
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construccion del lexer
lexer = lex.lex()

# Precedencia de operadores
precedence = (
    ('left', 'BICOND'),
    ('left', 'IMPLIES'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

# Clase para nodos del arbol sintactico
class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        if children is None:
            children = []
        self.children = children

# Reglas de la gramatica
def p_formula_var(p):
    'formula : VAR'
    p[0] = Node('VAR', p[1])

def p_formula_const(p):
    'formula : CONST'
    p[0] = Node('CONST', p[1])

def p_formula_not(p):
    'formula : NOT formula'
    p[0] = Node('OP', '~', [p[2]])

def p_formula_binop(p):
    '''formula : formula AND formula
               | formula OR formula
               | formula IMPLIES formula
               | formula BICOND formula'''
    p[0] = Node('OP', p[2], [p[1], p[3]])

def p_formula_paren(p):
    'formula : LPAREN formula RPAREN'
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Error de sintaxis en token '{p.value}'")
    else:
        print("Error de sintaxis al final de la entrada")

# Construccion del parser
parser = yacc.yacc()

# Funcion para generar el grafico del arbol sintactico
def generate_syntax_tree(node, dot=None):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='circle')
    
    if node.value is not None:
        label = node.value
    else:
        label = node.type
    
    dot.node(str(id(node)), label)
    
    for child in node.children:
        dot.edge(str(id(node)), str(id(child)))
        generate_syntax_tree(child, dot)
    
    return dot

# Funcion para generar el grafico del AFN usando expresiones regulares
def generate_afn_with_regex(expr):
    dot = Digraph()
    dot.attr('node', shape='circle')
    
    prev_state = "start"
    dot.node(prev_state, "start")
    
    for i, char in enumerate(expr):
        current_state = f"q{i}"
        dot.node(current_state, char)
        
        # Determinar la etiqueta de transicion basada en el caracter
        transition_label = None
        for token, regex in regex_map.items():
            if char in regex:
                transition_label = regex
                break
        
        if transition_label:
            dot.edge(prev_state, current_state, label=transition_label)
        else:
            dot.edge(prev_state, current_state, label=char)
        
        prev_state = current_state
    
    dot.node("accept", "accept")
    dot.edge(prev_state, "accept", label="ε")
    
    filename = f"afn_regex_{expr.replace(' ', '_').replace('(', '').replace(')', '')}"
    dot.render(filename, format='png', cleanup=True)
    print(f"AFN guardado como: {filename}.png")

# Funcion principal
def main():
    # Lista de expresiones a procesar
    expressions = [
        "p",
        "~q",
        "(p^q)",
        "(0=>(ros))",
        "^(p^q)",
        "(p<=>~p)",
        "((p=>q)^p)",
        "(*(p^(qor))os)"
    ]
    
    for expr in expressions:
        print(f"\n{'='*50}")
        print(f"Procesando expresion: '{expr}'")
        print(f"{'='*50}")
        
        # Tokenizacion
        lexer.input(expr)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append((tok.type, tok.value))
        
        print("\n> 1. Tokenizacion:")
        print("   ➡ Tokens generados:")
        for i, token in enumerate(tokens, start=1):
            print(f"      Token {i}: Tipo={token[0]}, Valor='{token[1]}'")
        
        # Generar grafico del AFN usando expresiones regulares
        generate_afn_with_regex(expr)
        
        # Analisis sintactico
        print("\n> 2. Analisis Sintactico:")
        try:
            ast = parser.parse(expr)
            print("   :) Expresion VALIDA")
            
            # Generar grafico del arbol sintactico
            dot = generate_syntax_tree(ast)
            filename = f"arbol_{expr.replace(' ', '_').replace('(', '').replace(')', '')}"
            dot.render(filename, format='png', cleanup=True)
            print(f"Arbol sintactico guardado como: {filename}.png")
        except Exception as e:
            print("   XXX Expresion INVALIDA")
            print(f"   Error: {str(e)}")
        
        # Preguntar al usuario si desea continuar
        user_input = input("\n¿Desea continuar con la siguiente expresion? (s/n): ").strip().lower()
        if user_input == 'n':
            print("Finalizando el programa.")
            break

if __name__ == '__main__':
    main()