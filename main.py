"""
-----------------------------------------------------------------------------
prtnumc.py


A simple demonstration of what an Abstract Syntax Tree can look like
-----------------------------------------------------------------------------

History:
           2024-02-14, DMW, extending ast_demo.py to be a print number language compiler
           2024-02-12, DMW, created
"""

import ply.lex as lex
import ply.yacc as yacc
from ASTNODE import ASTNODE
import logging

symbol_table = {
   0: {}
}
reserved = {
    'print': 'PRINT',
    'readLine': 'READLINE',
    'abs': 'ABS',
    'min': 'MIN',
    'max': 'MAX',
    'for': 'FOR',
    'while': 'WHILE',
    'let': 'LET',
    'var': 'VAR',
    'if': "IF",
    'else': "ELSE",
    'in': "IN",
      }

tokens = [
   'NUMBER',
   'SQ_STRING',
   'DQ_STRING',
   'DOUBLE_EQ',
   'NAME',
   'NOT_EQ',
   'LESS_EQ',
   'GREATER_EQ',
   'ELLIPSIS',
   'POWER'
   ]
tokens += list(reserved.values())

literals = ['(', ')', ';', '{', '}', '+', '-', '/', '%', '*', "=", '"', '<', '>', '!', ',']

def str_to_num(s):
   ans = 0
   try:
       ans = int(s)
   except ValueError:
       ans = float(s)

   return ans

def t_SQ_STRING(t):
    r"'[^'\\]*(?:\\.[^'\\]*)*'"
    return t

def t_DQ_STRING(t):
    r'"[^"\\]*(?:\\.[^"\\]*)*"'
    return t

def t_ELLIPSIS(t):
   "\.\.\."
   return t

def t_POWER(t):
   "\*\*"
   return t

def t_NUMBER(t):
   # https://www.regular-expressions.info/floatingpoint.html
   r'[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
   t.value = str_to_num(t.value) # int(t.value)
   return t

def t_DOUBLE_EQ(t):
    r'=='
    return t

def t_NOT_EQ(t):
    r'!='
    return t

def t_LESS_EQ(t):
    r'<='
    return t

def t_GREATER_EQ(t):
    r'>='
    return t

def t_PRINT(t):
   'print'
   return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
    return t

t_ignore = " \t\v\f"

def t_newline(t):
   r'\n+'
   t.lexer.lineno += t.value.count("\n")

def t_error(t):
   print("Illegal character '%s'" % t.value[0])
   t.lexer.skip(1)

precedence = (
    # ('nonassoc', '?', ':'), # 'EQUALS', 'LESSTHAN', 'GREATERTHAN', 'LTEQ', 'GTEQ',
    ('left', '+', '-'),
    ('left', 'ELLIPSIS'),
    ('left', '*', '/'),  # '%', 'INTDIV'),
    ("nonassoc", 'IF'),
    ('right', 'UMINUS')
)

# Build the lexer
lexer = lex.lex()

# ----------------------------------------- 2024-02-14, DMW, PARSER

program = None

branch_index = 0

def p_PROGRAM(p):
   "program : statement_list"
   global program
   program = ASTNODE("program", children=[p[1]])

def p_STATEMENT_LIST2(p):
   "statement_list : statement_list statement"  # 2024-02-14, DMW, changed the print grammar to the following
   p[0] = ASTNODE("statement_list", children=[p[1], p[2]])

def p_STATEMENT_LIST(p):
   "statement_list : statement"  # 2024-02-14, DMW, changed the print grammar to the following
   p[0] = p[1]

def p_FOR(p):
   "for : FOR for_assign IN expression statement_block"
   global branch_index
   branch_index+=1
   p[0] = ASTNODE("for", children=[p[4], p[5]], data={"var_name":p[2].data["var_name"], "branch_index":branch_index})

def p_WHILE(p):
   "for : WHILE expression statement_block"
   global branch_index
   branch_index+=1
   p[0] = ASTNODE("while", children=[p[2], p[3]], data={"branch_index":branch_index})

def p_STATEMENT_ASSIGN(p):
   "statement : assign"  # 2024-02-14, DMW, changed the print grammar to the following
   p[0] = ASTNODE("statement", children=[p[1]])

def p_LET_ASSIGN(p):
   "assign : LET NAME '=' expression"
   global branch_index
   branch_index+=1
   symbol_table[0][p[2]] = {"var_name": f"{p[2]}_{branch_index}", "type":p[4].data["type"]}
   p[0] = ASTNODE("assign", children=[p[4]], data={"var_name":f"{p[2]}_{branch_index}", "type":p[4].data["type"]})

def p_VAR_ASSIGN(p):
   "assign : VAR NAME '=' expression"
   global branch_index
   branch_index+=1
   symbol_table[0][p[2]] = {"var_name": f"{p[2]}_{branch_index}", "type":p[4].data["type"]}
   p[0] = ASTNODE("assign", children=[p[4]], data={"var_name":f"{p[2]}_{branch_index}", "type":p[4].data["type"]})

def p_REASSIGN(p):
   "assign : NAME '=' expression"
   var_name = symbol_table[0][p[1]]["var_name"]
   p[0] = ASTNODE("assign", children=[p[3]], data={"var_name":var_name})

def p_STATEMENT_BLOCK(p):
    "statement_block : '{' statement_list '}'"
    p[0] = ASTNODE("statement_block", children=[p[2]])

def p_FOR_ASSIGN(p):
   "for_assign : NAME"
   global branch_index
   branch_index+=1
   symbol_table[0][p[1]] = {"var_name": f"{p[1]}_{branch_index}", "type": "int"}
   p[0] = ASTNODE("for_assign", data={"var_name":symbol_table[0][p[1]]["var_name"]})

def p_STATEMENT_BLOCK2(p):
    "statement_block : statement"
    p[0] = p[1]

def p_STATEMENT_PRINT(p):
   "statement : print"  # 2024-02-14, DMW, changed the print grammar to the following
   p[0] = ASTNODE("statement", children=[p[1]])

def p_STATEMENT_COMPARISON(p):
   "statement : expression"  # 2024-02-14, DMW, changed the print grammar to the following
   p[0] = ASTNODE("statement", children=[p[1]])

def p_STATEMENT_FOR(p):
    "statement : for"
    p[0] = p[1]

def p_PRINT_STATEMENT(p):
   """print : PRINT '(' print_expression_list ')' """
   p[0] = ASTNODE("print_list", children=[p[3]])

def p_PRINT_STATEMENT2(p):
   """print : PRINT '(' expression ')' """
   p[0] = ASTNODE("print", children=[p[3]])

def p_EXPRESSION_INPUT(p):
   "expression : READLINE '(' ')'"  # 2024-02-14, DMW, changed the print grammar to the following
   global branch_index
   branch_index+=1
   p[0] = ASTNODE("input", data={"type":"int"})

def p_EXPRESSION_MIN(p):
   "expression : MIN '(' expression ',' expression ')'"  # 2024-02-14, DMW, changed the print grammar to the following
   global branch_index
   branch_index+=1
   p[0] = ASTNODE("min", children=[p[3], p[5]], data={"branch_index": branch_index})

def p_EXPRESSION_MAX(p):
   "expression : MAX '(' expression ',' expression ')'"  # 2024-02-14, DMW, changed the print grammar to the following
   global branch_index
   branch_index+=1
   p[0] = ASTNODE("max", children=[p[3], p[5]], data={"branch_index": branch_index})

def p_EXPRESSION_ABS(p):
   "expression : ABS '(' expression ')'"  # 2024-02-14, DMW, changed the print grammar to the following
   p[0] = ASTNODE("abs", children=[p[3]], data={"branch_index": branch_index})

def p_EXPRESSION_POWER(p):
   "expression : expression POWER expression"
   global branch_index
   branch_index+=1
   if p[1].data["type"] != "int" or p[3].data["type"] != "int":
      raise Exception("Invalid types for binary operation.") 
   p[0] = ASTNODE("exponent", data={"type":"int", "branch_index": branch_index}, children=[p[1], p[3]])

def p_EXPRESSION_UMINUS(p):
   """expression : '-' expression %prec UMINUS"""
   if p[2].data["type"] != "int":
      raise Exception("Invalid type for unary minus operation.")
   p[0] = ASTNODE("uminus", children=[p[2]], data={"type": "int"})

def p_EXPRESSION_BINOP(p):
   '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '%' expression'''
   if p[1].data["type"] != "int" or p[3].data["type"] != "int":
      raise Exception("Invalid types for binary operations.")
   if not p[1].children and not p[3].children:
      p[0] = ASTNODE("number", value=p[1].value + p[3].value, data={"type": "int"})
   else:
      p[0] = ASTNODE("binop", value=p[2], children=[p[1], p[3]], data={"type": "int"})

def p_EXPRESSION_RANGE(p):
   "expression : expression ELLIPSIS expression"
   if p[1].data["type"] != "int" or p[3].data["type"] != "int":
      raise Exception("Invalid types for range operation.")
   p[0] = ASTNODE("range", value=p[2], children=[p[1], p[3]])

def p_EXPRESSION_NUM(p):
   "expression : NUMBER"
   try:
      int(p[1])
   except Exception as e:
      raise Exception
      
   p[0] = ASTNODE("number", value=p[1], data={"type": "int"})

def p_EXPRESSION_NAME(p):
   "expression : NAME"
   p[0] = ASTNODE("name", data={"var_name":symbol_table[0][p[1]]["var_name"], "type": symbol_table[0][p[1]]["type"]})

def remove_quotes(s):
    return s[1:-1]

def p_EXPRESSION_DQ_STRING(p):
   "expression : DQ_STRING"
   p[0] = ASTNODE("string", value=remove_quotes(p[1]), data={"type": "string"})

def p_EXPRESSION_SQ_STRING(p):
   "expression : SQ_STRING"
   p[0] = ASTNODE("string", value=remove_quotes(p[1]), data={"type": "string"})

def p_EXPRESSION_GROUP(p):
   "expression : '(' expression ')'"
   p[0] = p[2]

def p_EXPRESSION_COMPARE(p):
   """expression : expression DOUBLE_EQ expression 
                 | expression NOT_EQ expression
                 | expression '>' expression
                 | expression '<' expression
                 | expression LESS_EQ expression
                 | expression GREATER_EQ expression
                   """
   global branch_index
   branch_index+=1
   if p[1].data["type"] != p[3].data["type"]:
      raise Exception("Incompatible types for comparison operation.")
   p[0] = ASTNODE("comparison", value=p[2], children=[p[1], p[3]], data={"branch_index": branch_index})

def p_IF_CONDITIONAL(p):
   """statement : IF  expression '{' statement_block '}'"""
   global branch_index
   branch_index+=1
   p[0] = ASTNODE("if", children=[p[2], p[4]], data={"branch_index": branch_index})

def p_IF_ELSE_CONDITIONAL(p):
   """statement : IF expression '{' statement '}' ELSE '{' statement_block '}'"""
   global branch_index
   branch_index+=1
   p[0] = ASTNODE("ifelse", children=[p[2], p[4], p[8]], data={"branch_index": branch_index})

def p_EMPTY_PRINT_LIST(p):
   """print_expression_list : """
   p[0] = ASTNODE("empty_list")

def p_PRINT_EXPRESSION_LIST(p):
   """print_expression_list : print_expression_list print_expression"""
   p[0] = ASTNODE("print_list", children=[p[1], p[2]])

def p_PRINT_EXPRESSION_LIST2(p):
   """print_expression_list : print_expression"""
   p[0] = p[1]

def p_PRINT_EXPRESSION(p):
   """print_expression : expression ',' """
   p[0] = ASTNODE("print", children=[p[1]])

def p_error(p):
   if p:
       print("Syntax error at '%s'" % p.value)
   else:
       print("Syntax error at EOF")


parser = yacc.yacc()
log = logging.getLogger()

if __name__ == "__main__":
   program = open('program.txt', 'r', encoding="utf8")
   program = program.read()
   yacc.parse(program, debug=log)
   ASTNODE.initialize_variables(symbol_table)
   print(".text")
   ASTNODE.emit_ast(program)
   print("li $v0, 10")
   print("syscall")

