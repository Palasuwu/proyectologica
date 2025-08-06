import ply.lex as lex
import ply.yacc as yacc
from graphviz import Digraph

# 1. Definición de tokens
tokens = (
    'VAR', 'CONST', 'NOT', 'AND', 'OR', 'IMPLIES', 'BICOND', 'LPAREN', 'RPAREN'
)

# 2. Expresiones regulares para tokens
t_VAR = r'[p-z]'
t_CONST = r'[01]'
t_NOT = r'~'
t_AND = r'\^'
t_OR = r'o'
t_IMPLIES = r'=>'
t_BICOND = r'<=>'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# 3. Ignorar espacios y tabulaciones
t_ignore = ' \t'

# 4. Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# 5. Construcción del lexer
lexer = lex.lex()

# 6. Precedencia de operadores
precedence = (
    ('left', 'BICOND'),
    ('left', 'IMPLIES'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

# 7. Clase para nodos del árbol sintáctico
class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        if children is None:
            children = []
        self.children = children

# 8. Reglas de la gramática
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

# 9. Construcción del parser
parser = yacc.yacc()

# 10. Función para generar gráfico del árbol sintáctico
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

# 11. Función para generar gráfico del AFN
def generate_afn(tokens, expr):
    dot = Digraph()
    dot.attr('node', shape='circle')
    
    prev_state = "start"
    dot.node(prev_state, "start")
    
    for i, token in enumerate(tokens):
        current_state = f"q{i}"
        dot.node(current_state, token[1])
        dot.edge(prev_state, current_state, label=token[0])
        prev_state = current_state
    
    dot.node("accept", "accept")
    dot.edge(prev_state, "accept", label="ε")
    
    filename = f"afn_{expr.replace(' ', '_').replace('(', '').replace(')', '')}"
    dot.render(filename, format='png', cleanup=True)
    print(f"AFN guardado como: {filename}.png")

# 12. Función principal
def main():
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
        print(f"Procesando expresión: '{expr}'")
        print(f"{'='*50}")
        
        # Análisis léxico
        lexer.input(expr)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append((tok.type, tok.value))
        
        print("\nTokens generados:")
        for token in tokens:
            print(f"  {token[0]}: {token[1]}")
        
        # Generar gráfico del AFN
        generate_afn(tokens, expr)
        
        # Análisis sintáctico
        try:
            ast = parser.parse(expr)
            print("\nExpresión VÁLIDA")
            
            # Generar gráfico del árbol sintáctico
            dot = generate_syntax_tree(ast)
            filename = f"arbol_{expr.replace(' ', '_').replace('(', '').replace(')', '')}"
            dot.render(filename, format='png', cleanup=True)
            print(f"Árbol sintáctico guardado como: {filename}.png")
        except Exception as e:
            print("\nExpresión INVÁLIDA")
            print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()