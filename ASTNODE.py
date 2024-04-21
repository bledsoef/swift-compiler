#  Author:  Deanna M. Wilborne
# College:  Berea College
#  Course:  CSC386 Fall 2021
# Purpose:  AST Node Class
# History:
#           2024-02-12, DMW, modified for CSC486 Compiler Design & Implementation
#           2023-04-30, DMW, conditionally import curses if not on Windows
#           2023-04-24, DMW, added __str__ method() for pretty printing nodes; imports curses.ascii and Common
#           2023-04-16, DMW, extra fields added to nodes, line, and index, for additional diagnostics
#           2023-04-04, DMW, updated for 2023-Summer CSC420 Programming Languages
#           2021-10-28, DMW, corrected an issue with __init__ where valid values of 0 wouldn't be saved in the node
#           2021-10-21, DMW, created
#
#           Copyright (2023) Deanna M. Wilborne

from anytree import NodeMixin, RenderTree
from Common import Common
from sys import platform

if platform != "win32":
    import curses.ascii as ca


# noinspection SpellCheckingInspection
class ASTNODE(NodeMixin):
    def __init__(self, name: str, value=None, parent=None, children=None, line=None, data={}) -> None:
        self.name = name
        self.parent = parent
        self.value = value
        # 2023-04-16, DWM, line and index is based on:
        # https://my.eng.utah.edu/~cs3100/lectures/l14/ply-3.4/doc/ply.html#ply_nn33
        self.line = line
        self.data = data


        if children is not None:
            self.children = children

    # 2023-04-24, DMW, substitute control characters in value attibutes of type string
    def safe_value(self) -> str:
        output = ""
        for char in self.value:
            output += ca.unctrl(char)
        return output

    # 2023-04-24, DMW, provide ability to print node details
    def __str__(self) -> str:
        output_str = "{" + " name='{}'".format(self.name)
        if self.value is not None:
            if platform != "win32":
                if Common.object_type(self.value) == "str":
                    output_str += ", value='{}'".format(self.safe_value())
                else:
                    output_str += ", value='{}'".format(self.value)
            else:
                output_str += ", value='{}'".format(self.value)
        if self.parent is not None:
            output_str += ", parent='{}'".format(self.parent.name)
        if self.children is not None:
            if len(self.children) != 0:
                children = ""
                for child in self.children:
                    if children != "":
                        children += ", '{}'".format(child.name)
                    else:
                        children = "[ '{}'".format(child.name)
                children += " ]"
                output_str += ", children={}".format(children)
        if self.line is not None:
            output_str += ", line={}".format(self.line)
        output_str += " }"
        return output_str

    # 2024-02-12, DMW, added class static method
    @staticmethod
    def render_tree(tree) -> None:
        for pre, fill, node in RenderTree(tree):
            print("%s%s" % (pre, node.name))

    @staticmethod
    def emit_ast(_node):
        if _node.name == "program":
            for child in _node.children:
                ASTNODE.emit_ast(child)
        elif _node.name == "statement_list":
            for child in _node.children:
                ASTNODE.emit_ast(child) 
        elif _node.name == "statement":
            for child in _node.children:
                ASTNODE.emit_ast(child)
        elif _node.name == "statement_block":
            for child in _node.children:
                ASTNODE.emit_ast(child)
        elif _node.name == "while":
            data = _node.data
            branch_index = data["branch_index"]
            print(f"loop_{branch_index}: # initialize loop branch")
            ASTNODE.emit_ast(_node.children[0])
            print("lw $t4, 4($sp) # pop an integer off the stack and load it into t4")
            print("addi $sp, $sp, 4")
            print(f"beq $t4, 0, continue_{branch_index} # if t4 == 0 move to the continue_{branch_index} branch")
            ASTNODE.emit_ast(_node.children[1])
            print(f"j loop_{branch_index} # jump to the loop_{branch_index} branch")
            print(f"continue_{branch_index}: # define a branch for the following code to continue")
        elif _node.name == "for":
            ASTNODE.emit_ast(_node.children[0])
            data = _node.data
            branch_index = data["branch_index"]
            var_name = data["var_name"]
            print("lw $t7, 4($sp) # pop the integer off the stack and load into t2")
            print("addi $sp, $sp, 4")
            print("lw $t6, 4($sp) # pop the integer off the stack and store it into t1")
            print("addi $sp, $sp, 4")
            print(f"sw $t6, {var_name} # store the value of {var_name} in t1")
            print(f"loop_{branch_index}: # create a loop branch")
            ASTNODE.emit_ast(_node.children[1])
            print("   addi $t6, $t6, 1")
            print(f"   sw $t6, {var_name} # store the value of {var_name} in t1")
            print(f"   bge $t7, $t6, loop_{branch_index} # if t2 is greater than or equal to t1 branch to loop_{branch_index}")

        elif _node.name == "conditional":
            pass
        elif _node.name == "for_assign":
            pass
        elif _node.name == "assign":
            data = _node.data
            var_name = data["var_name"]
            for child in _node.children:
                ASTNODE.emit_ast(child)
            print("lw $t0, 4($sp) # pop an integer off the stack and store in t0")
            print("addi $sp, $sp, 4")
            print(f"sw $t0, {var_name} # store t0 in {var_name}")
        elif _node.name == "range":
            for child in _node.children:
                ASTNODE.emit_ast(child)
        elif _node.name == "input":
            print("li $v0, 5 # load the integer 5 into v0 to accept a user integer input")
            print("syscall")
            print("move $t0, $v0 # move the value of v0 into t0")
            print("addi $sp, $sp, -4")
            print("sw $t0, 4($sp) # store t0 on the stack")
        elif _node.name == "print":
            for child in _node.children:
                ASTNODE.emit_ast(child)
            print("lw $a0, 4($sp) # pop a value off the stack and store it on a0")
            print("addi $sp, $sp, 4")
            print("li $v0, 1 # load 1 into v0 for an integer print syscall")
            print("syscall")
            print("li $a0, 10")
            print("li $v0, 11 # print a newline")
            print("syscall")
            print("li $a0, 0")
        elif _node.name == "expression":
            for child in _node.children:
                ASTNODE.emit_ast(child)
        elif _node.name == "binop":
            for child in _node.children:
                ASTNODE.emit_ast(child)
            print("lw $t0, 4($sp)")
            print("addi $sp, $sp, 4")
            print("lw $t1, 4($sp)")
            print("addi $sp, $sp, 4")
            if _node.value == "+":
                print("add $t2, $t1, $t0")
            elif _node.value == "-":
                print("sub $t2, $t1, $t0")
            elif _node.value == "*":
                print("mult $t1, $t0")
                print("mflo $t2")
            elif _node.value == "/":
                print("div $t2, $t1, $t0")
            print("addi $sp, $sp, -4")
            print("sw $t2, 4($sp)")
            print("li $t2, 0")
        elif _node.name == "if":
            data = _node.data
            branch_index = data["branch_index"]
            ASTNODE.emit_ast(_node.children[0])
            
            print("lw $t0, 4($sp)")  
            print("addi $sp, $sp, 4")
            print(f"beq $t0, 1, true_{branch_index}")
            print(f"false_{branch_index}:")
            print(f"     j continue_{branch_index}")
            print(f"true_{branch_index}:")
            
            ASTNODE.emit_ast(_node.children[1])
            print(f"continue_{branch_index}:")
            print("addi $sp, $sp, -4")
            print("sw $t2, 4($sp)")
            print("li $t2, 0")
        elif _node.name == "ifelse":
            data = _node.data
            branch_index = data["branch_index"]
            ASTNODE.emit_ast(_node.children[0])
            
            print("lw $t0, 4($sp)")  
            print("addi $sp, $sp, 4")
            print(f"beq $t0, 1, true_{branch_index}")
            print(f"false_{branch_index}:")
            ASTNODE.emit_ast(_node.children[2])
            print(f"     j continue_{branch_index}")
            print(f"true_{branch_index}:")
            
            ASTNODE.emit_ast(_node.children[1])
            print(f"continue_{branch_index}:")
            print("addi $sp, $sp, -4")
            print("sw $t2, 4($sp)")
            print("li $t2, 0")
        elif _node.name == "abs":
            for child in _node.children:
                ASTNODE.emit_ast(child)
            data = _node.data
            branch_index = data["branch_index"]
            print(f"bge $t0, $zero, continue_{branch_index}")
            print(f"negate_{branch_index}:")
            print("li $t1, -1")
            print("mult $t0, $t1")
            print("mflo $t0")
            print(f"continue_{branch_index}:")
            print("addi $sp, $sp, -4")
            print("sw $t0, 4($sp)")            
        elif _node.name == "min":
            for child in _node.children:
                ASTNODE.emit_ast(child)
            data = _node.data
            branch_index = data["branch_index"]
            print("lw $t0, 4($sp)")  
            print("addi $sp, $sp, 4")
            print("lw $t1, 4($sp)")  
            print("addi $sp, $sp, 4")
            print(f"bge $t0, $t1, second_{branch_index}")
            print(f"first_{branch_index}:")
            print("move $t2, $t0")
            print(f"j continue_{branch_index}")
            print(f"second_{branch_index}:")
            print("move $t2, $t1")
            print(f"continue_{branch_index}:")
            print("addi $sp, $sp, -4")
            print("sw $t2, 4($sp)")
        elif _node.name == "max":
            for child in _node.children:
                ASTNODE.emit_ast(child)
            data = _node.data
            branch_index = data["branch_index"]  
            print("lw $t0, 4($sp)")  
            print("addi $sp, $sp, 4")
            print("lw $t1, 4($sp)")  
            print("addi $sp, $sp, 4")
            print(f"ble $t0, $t1, second_{branch_index}")
            print(f"first_{branch_index}:")
            print("move $t2, $t0")
            print(f"j continue_{branch_index}")
            print(f"second_{branch_index}:")
            print("move $t2, $t1")
            print(f"continue_{branch_index}:")
            print("addi $sp, $sp, -4")
            print("sw $t2, 4($sp)")
            print("l2 $t0, 0")
        elif _node.name == "exponent":
            for child in _node.children:
                ASTNODE.emit_ast(child)
            data = _node.data
            branch_index = data["branch_index"]  
            print("li      $t0, 1 # res = 1")
            print("li      $t1, 1 # iterator = 1")
            print("lw $t2, 4($sp)")  
            print("addi $sp, $sp, 4")
            print("lw $t3, 4($sp)")  
            print("addi $sp, $sp, 4")

            print(f"loop_{branch_index}:") 

            print("mult     $t0, $t3  # res * iterator")
            print("mflo $t0")
            print("add      $t1, $t1, 1")
            print(f"ble     $t1, $t2, loop_{branch_index}")
                    
            print("addi $sp, $sp, -4")
            print("sw $t0, 4($sp)")

        elif _node.name == "comparison":
            data = _node.data
            branch_index = data["branch_index"]            
            for child in _node.children:
                ASTNODE.emit_ast(child)
            print("lw $t0, 4($sp)")  
            print("addi $sp, $sp, 4")
            print("lw $t1, 4($sp)")
            print("addi $sp, $sp, 4")
            if _node.value == "==":
                print(f"beq $t0, $t1, true_{branch_index}")
            elif _node.value == "<":
                print(f"bgt $t0, $t1, true_{branch_index}")

            elif _node.value == "<=":
                print(f"bge $t0, $t1, true_{branch_index}")

            elif _node.value == ">":
                print(f"blt $t0, $t1, true_{branch_index}")
            elif _node.value == ">=":
                print(f"ble $t0, $t1, true_{branch_index}")

            print(f"false_{branch_index}:")
            print("     li $t2, 0")
            print(f"     j continue_{branch_index}")
            print(f"true_{branch_index}:")
            print("     li $t2, 1")
            print(f"continue_{branch_index}:")
            print("addi $sp, $sp, -4")
            print("sw $t2, 4($sp)")
            print("li $t2, 0")
        elif _node.name == "print_list":
            for child in _node.children:
                ASTNODE.emit_ast(child)
        elif _node.name == "uminus":
            for child in _node.children:
                ASTNODE.emit_ast(child)
            print("lw $t0, 4($sp) # pop an integer off the stack and store it in 10")  
            print("addi $sp, $sp, 4")
            print("li $t1, -1 # load -1 into t1")
            print("mult $t0, $t1 # multiply t0 and t1")
            print("mflo $t0")
            print("addi $sp, $sp, -4")
            print("sw $t0, 4($sp) # store t0 onto the stack")
            print("li $t0, 0")
            print("li $t1, 0")
        elif _node.name == "name":
            data = _node.data
            var_name = data["var_name"]
            print(f"lw $t0, {var_name} # load the value of {var_name} into t0")
            print("addi $sp, $sp, -4")
            print("sw $t0, 4($sp) # store the value of t0 on the stack")        
            print("li $t0, 0")
        elif _node.name == "number":
            print("li $t0, {} # load an integer into t0".format(_node.value))
            print("addi $sp, $sp, -4")
            print("sw $t0, 4($sp) # store the integer on the stack")
            print("li $t0, 0")
        elif _node.name == "string":
            print("li $t0, {} # store a string into t0".format(_node.value))
            print("addi $sp, $sp, -4")
            print("sw $t0, 4($sp) # put the value of sw t0 onto the stack")
    @staticmethod
    def initialize_variables(symbol_table) -> None:
        print(".data")
        for scope, data in symbol_table.items():
            for variable, values in data.items():
                print(f"{values['var_name']}: .word 0")

# limited functional testing
# 2023-04-24, DMW, updated to use test() to prevent pycharm warnings about shadowing "child"
if __name__ == "__main__":
    def test():
        child2 = ASTNODE("child2")
        child3 = ASTNODE("child3")
        child = ASTNODE("child", children=[child2, child3])
        root = ASTNODE("root", value="\ntest\n", children=[child])
        ASTNODE.render_tree(root)

    test()

