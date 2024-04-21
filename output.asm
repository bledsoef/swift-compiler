.data
.text
li $t0, 10 # load an integer into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the integer on the stack
li $t0, 0
li $t0, 2 # load an integer into t0
addi $sp, $sp, -4
sw $t0, 4($sp) # store the integer on the stack
li $t0, 0
li      $t0, 1 # res = 1
li      $t1, 1 # iterator = 1
lw $t2, 4($sp)
addi $sp, $sp, 4
lw $t3, 4($sp)
addi $sp, $sp, 4
loop_1:
mult     $t0, $t3  # res * iterator
mflo $t0
add      $t1, $t1, 1
ble     $t1, $t2, loop_1
addi $sp, $sp, -4
sw $t0, 4($sp)
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
