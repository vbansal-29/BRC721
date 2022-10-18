.globl write_matrix

.text
# ==============================================================================
# FUNCTION: Writes a matrix of integers into a binary file
# FILE FORMAT:
#   The first 8 bytes of the file will be two 4 byte ints representing the
#   numbers of rows and columns respectively. Every 4 bytes thereafter is an
#   element of the matrix in row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is the pointer to the start of the matrix in memory
#   a2 (int)   is the number of rows in the matrix
#   a3 (int)   is the number of columns in the matrix
# Returns:
#   None
# Exceptions:
#   - If you receive an fopen error or eof,
#     this function terminates the program with error code 27
#   - If you receive an fclose error or eof,
#     this function terminates the program with error code 28
#   - If you receive an fwrite error or eof,
#     this function terminates the program with error code 30
# ==============================================================================
write_matrix:
    addi sp, sp, -32
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    sw s2, 12(sp)
    sw s3, 16(sp)
    sw s4, 20(sp)
    sw s5, 24(sp)
    sw s6, 28(sp)
    
    mv s0, a0
    mv s1, a1
    mv s2, a2
    mv s3, a3
    
    addi a1, x0, 1
    jal ra, fopen
    li t0, -1
    beq a0, t0, error27
    mv s4, a0
    
    li a0 4
    jal ra, malloc
    mv s5 a0
    sw s2 0(s5)
    
    
    li a0 4
    jal ra, malloc
    mv s6 a0
    
    sw s3 0(s6)
    
    
    mv a0, s4
    mv a1, s5
    li a2 1
    addi sp sp -4
    sw a2 0(sp)
    li a3, 4
    jal ra, fwrite
    lw a2 0(sp)
    addi sp sp 4
    
    bne a0 a2 error30
    
    mv a0, s4
    mv a1, s6
    li a2 1
    addi sp sp -4
    sw a2 0(sp)
    li a3, 4
    jal ra, fwrite
    lw a2 0(sp)
    addi sp sp 4
    
    bne a0 a2 error30

    
    mv a0, s4
    mv a1, s1
    mul a2, s2, s3
    addi sp sp -4
    sw a2 0(sp)
    li a3, 4
    jal ra, fwrite
    lw a2 0(sp)
    addi sp sp 4
    bne a0 a2 error30

    ebreak
    mv a0, s4
    jal ra, fclose
    li t0, -1
    beq a0 t0 error28
    
    mv a0 s6
    jal ra, free
    mv a0 s5
    jal ra, free
    
    
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    lw s2, 12(sp)
    lw s3, 16(sp)
    lw s4, 20(sp)
    lw s5, 24(sp)
    lw s6, 28(sp)
    addi sp sp 32

    jr ra
    
error27:
    addi a0 x0 27
    j exit
error28:
    addi a0 x0 28
    j exit
error30:
    addi a0 x0 30
    j exit