.globl read_matrix

.text
# ==============================================================================
# FUNCTION: Allocates memory and reads in a binary file as a matrix of integers
#
# FILE FORMAT:
#   The first 8 bytes are two 4 byte ints representing the # of rows and columns
#   in the matrix. Every 4 bytes afterwards is an element of the matrix in
#   row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is a pointer to an integer, we will set it to the number of rows
#   a2 (int*)  is a pointer to an integer, we will set it to the number of columns
# Returns:
#   a0 (int*)  is the pointer to the matrix in memory
# Exceptions:
#   - If malloc returns an error,
#     this function terminates the program with error code 26
#   - If you receive an fopen error or eof,
#     this function terminates the program with error code 27
#   - If you receive an fclose error or eof,
#     this function terminates the program with error code 28
#   - If you receive an fread error or eof,
#     this function terminates the program with error code 29
# ==============================================================================
read_matrix:
    addi sp, sp, -32
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    sw s2, 12(sp)
    sw s3, 16(sp)
    sw s4 20(sp)
    sw s5 24(sp)
    sw s6 28(sp)
    
    addi s0, a0, 0
    addi s1, a1, 0
    addi s2, a2, 0
    
    add a1, x0, x0
    
    jal ra, fopen
    
    addi t0, x0, -1
    beq a0, t0, error27
    add s3, a0, x0
    
    add a1, x0, s1
    addi a2, x0, 4
    addi sp, sp, -4
    sw a2, 0(sp)
    jal ra, fread
    lw a2, 0(sp)
    addi sp, sp, 4
    bne a0, a2, error29
    lw s6, 0(s1)
    
    add a0 s3 x0
    add a1, x0, s2
    addi a2, x0, 4
    addi sp, sp, -4
    sw a2, 0(sp)
    jal ra, fread
    lw a2, 0(sp)
    addi sp, sp, 4
    bne a0, a2, error29

    lw t2, 0(s2)
    addi t0, x0, 0
    add a1, s6, t0
    add a2, t2, t0
    addi t0, x0, 4
    mul a0, a1, a2
    mul a0, a0, t0
    add s5 a0 x0
    jal ra, malloc
    beq a0 x0 error26
    add s4, a0, x0
    
    add a0 s3 x0
    add a1 s4 x0
    add a2 s5 x0
    addi sp, sp, -4
    sw a2, 0(sp)
    jal ra, fread
    lw a2, 0(sp)
    addi sp, sp, 4
    bne a0, a2, error29
    
    add a0 x0 s3
    jal ra, fclose
    addi t0, x0, -1
    beq a0, t0, error28
    
    
    add a1, x0, s1
    add a2, x0, s2
    
    add a0 x0 s4
    
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    lw s2, 12(sp)
    lw s3, 16(sp)
    lw s4 20(sp)
    lw s5 24(sp)
    lw s6 28(sp)
    addi sp, sp, 32
    jr ra

error28:
    addi a0, x0, 28
    j exit
    
error27:
    addi a0, x0, 27
    j exit

error26:
    addi a0, x0, 26
    j exit
    
error29:
    addi a0, x0, 29
    j exit
    
    
