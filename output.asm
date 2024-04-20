.data
.text
li $t0, 10
addi $sp, $sp, -4
sw $t0, 4($sp)
lw $t0, 4($sp)
addi $sp, $sp, 4
li $t1, -1
mult $t0, $t1
mflo $t0
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 10
addi $sp, $sp, -4
sw $t0, 4($sp)
lw $t0, 4($sp)
addi $sp, $sp, 4
lw $t1, 4($sp)
addi $sp, $sp, 4
ble $t0, $t1, second_1
first_1:
move $t2, $t0
j continue_1
second_1:
move $t2, $t1
continue_1:
addi $sp, $sp, -4
sw $t2, 4($sp)
lw $a0, 4($sp)
addi $sp, $sp, 4
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall
li $v0, 10
syscall
