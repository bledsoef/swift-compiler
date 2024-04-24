hi
hi
.data
.text
li $t0, 18 # load an integer into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the integer on the stack
li $t0, 0
lw $a0, 4($sp) # pop a value off the stack and store it on a0
addi $sp, $sp, 4
li $v0, 1 # load 1 into v0 for an integer print syscall
syscall
li $a0, 10
li $v0, 11 # print a newline
syscall
li $a0, 0
li $v0, 10
syscall
