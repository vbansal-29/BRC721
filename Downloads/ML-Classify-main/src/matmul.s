.globl matmul

.text
# =======================================================
# FUNCTION: Matrix Multiplication of 2 integer matrices
#   d = matmul(m0, m1)
# Arguments:
#   a0 (int*)  is the pointer to the start of m0
#   a1 (int)   is the # of rows (height) of m0
#   a2 (int)   is the # of columns (width) of m0
#   a3 (int*)  is the pointer to the start of m1
#   a4 (int)   is the # of rows (height) of m1
#   a5 (int)   is the # of columns (width) of m1
#   a6 (int*)  is the pointer to the the start of d
# Returns:
#   None (void), sets d = matmul(m0, m1)
# Exceptions:
#   Make sure to check in top to bottom order!
#   - If the dimensions of m0 do not make sense,
#     this function terminates the program with exit code 38
#   - If the dimensions of m1 do not make sense,
#     this function terminates the program with exit code 38
#   - If the dimensions of m0 and m1 don't match,
#     this function terminates the program with exit code 38
# =======================================================
matmul:
    # Error checks
    blt a1 x0 error
    blt a2 x0 error
    blt a4 x0 error
    blt a5 x0 error
    beq a1 x0 error
    beq a2 x0 error
    beq a4 x0 error
    beq a5 x0 error
    bne a2 a4 error
    
    addi sp, sp, -32
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw s4, 16(sp)
    sw s5, 20(sp)
    sw s6, 24(sp)
    sw ra, 28(sp)
    
    mv s0, a0
    mv s1, a1
    mv s2, a2
    mv s3, a3
    mv s4, a4
    mv s5, a5
    mv s6, a6
   
    
    # Prologue
    li x3 0 # counter outer loop
    li t4 4 # incrementer by 4
    
    addi a3 x0 1
    add a4 x0 a5
    
    
outer_loop_start:
    beq x3 s1 outer_loop_end
    li x1 0 # counter inner loop
    li t1 0 # counter column in inner
    
    add a1 x0 s3


inner_loop_start:
    beq x1 s5 inner_loop_end
    addi sp sp -32
    sw a0 0(sp)
    sw x1 4(sp)
    sw a6 8(sp)
    sw a1 12(sp)
    sw t4 16(sp)
    sw a2 20(sp)
    sw a3 24(sp)
    sw a4 28(sp)
    
    jal ra, dot
    lw a6 8(sp)
    sw a0 0(a6)
    addi a6 a6 4
    
    lw a0 0(sp)
    lw x1 4(sp)
    lw a1 12(sp)
    lw t4 16(sp)
    lw a2 20(sp)
    lw a3 24(sp)
    lw a4 28(sp)
    addi sp sp 32
    add a1 a1 t4
    addi x1 x1 1
    
    j inner_loop_start
    
inner_loop_end:
    mul t2 s2 t4
    add a0 a0 t2
    
    addi x3 x3 1
    j outer_loop_start

outer_loop_end:   
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw s4, 16(sp)
    lw s5, 20(sp)
    lw s6, 24(sp)
    lw ra, 28(sp)
    addi sp, sp, 32
    ret

error:
    li a0 38
    j exit
