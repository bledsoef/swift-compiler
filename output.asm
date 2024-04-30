.data
counter_1: .word 0
.text
li $t0, 18 # load an integer into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the integer on the stack
li $t0, 0
lw $t0, 4($sp) # pop an integer off the stack and store in t0
addi $sp, $sp, 4
sw $t0, counter_1 # store t0 in counter_1
lw $t0, counter_1 # load the value of counter_1 into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the value of t0 on the stack
li $t0, 0
lw $a0, 4($sp) # pop a value off the stack and store it on a0
addi $sp, $sp, 4
li $v0, 1 # load 1 into v0 for an integer print syscall
syscall
li $a0, 10
li $v0, 11 # print a newline
syscall
li $a0, 0
loop_3: # initialize loop branch
lw $t0, counter_1 # load the value of counter_1 into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the value of t0 on the stack
li $t0, 0
li $t0, 0 # load an integer into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the integer on the stack
li $t0, 0
lw $t0, 4($sp)
addi $sp, $sp, 4
lw $t1, 4($sp)
addi $sp, $sp, 4
blt $t0, $t1, true_2
false_2:
     li $t2, 0
     j continue_2
true_2:
     li $t2, 1
continue_2:
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 0
lw $t4, 4($sp) # pop an integer off the stack and load it into t4
addi $sp, $sp, 4
beq $t4, 0, continue_3 # if t4 == 0 move to the continue_3 branch
lw $t0, counter_1 # load the value of counter_1 into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the value of t0 on the stack
li $t0, 0
li $t0, 1 # load an integer into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the integer on the stack
li $t0, 0
lw $t0, 4($sp)
addi $sp, $sp, 4
lw $t1, 4($sp)
addi $sp, $sp, 4
sub $t2, $t1, $t0
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 0
lw $t0, 4($sp) # pop an integer off the stack and store in t0
addi $sp, $sp, 4
sw $t0, counter_1 # store t0 in counter_1
j loop_3 # jump to the loop_3 branch
continue_3: # define a branch for the following code to continue
lw $t0, counter_1 # load the value of counter_1 into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the value of t0 on the stack
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
