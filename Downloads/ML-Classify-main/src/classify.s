.globl classify

.text
# =====================================
# COMMAND LINE ARGUMENTS
# =====================================
# Args:
#   a0 (int)        argc
#   a1 (char**)     argv
#   a1[1] (char*)   pointer to the filepath string of m0
#   a1[2] (char*)   pointer to the filepath string of m1
#   a1[3] (char*)   pointer to the filepath string of input matrix
#   a1[4] (char*)   pointer to the filepath string of output file
#   a2 (int)        silent mode, if this is 1, you should not print
#                   anything. Otherwise, you should print the
#                   classification and a newline.
# Returns:
#   a0 (int)        Classification
# Exceptions:
#   - If there are an incorrect number of command line args,
#     this function terminates the program with exit code 31
#   - If malloc fails, this function terminates the program with exit code 26
#
# Usage:
#   main.s <M0_PATH> <M1_PATH> <INPUT_PATH> <OUTPUT_PATH>
classify:
    ebreak

    addi sp sp -52
    sw ra 0(sp)
    sw s1 4(sp)
    sw s2 8(sp)
    sw s3 12(sp)
    sw s4 16(sp)
    sw s5 20(sp)
    sw s6 24(sp)
    sw s7 28(sp)
    sw s8 32(sp)
    sw s9 36(sp)
    sw s10 40(sp)
    sw s11 44(sp)
    sw s0 48(sp)
    
    
    li t0 5
    bne a0 t0 error31
    
    mv s0 a2
    
    # Read pretrained m0
    mv s1, a1
    li a0 4
    jal ra, malloc
#     jal ra, randomizeCallerSavedRegsBesidesA0
    beq a0 x0 error26
    mv s2 a0
    li a0 4
    
    jal ra, malloc
    beq a0 x0 error26
    mv s3 a0
    lw a0 4(s1)
    mv a1 s2
    mv a2 s3
    jal ra, read_matrix
#     jal ra, randomizeCallerSavedRegsBesidesA0
    mv s4 a0
 
    # Read pretrained m1
    li a0 4
    jal ra, malloc
#     jal ra, randomizeCallerSavedRegsBesidesA0
    beq a0 x0 error26
    mv s5 a0
    li a0 4
    jal ra, malloc
#     jal ra, randomizeCallerSavedRegsBesidesA0
    beq a0 x0 error26
    mv s6 a0
    lw a0 8(s1)
    mv a1 s5
    mv a2 s6
    jal ra, read_matrix
#     jal ra, randomizeCallerSavedRegsBesidesA0
    mv s7 a0
    ebreak
  
    # Read input matrix 
    li a0 4
    jal ra, malloc
#     jal ra, randomizeCallerSavedRegsBesidesA0
    beq a0 x0 error26
    mv s8 a0
    li a0 4
    jal, ra malloc
#     jal ra, randomizeCallerSavedRegsBesidesA0
    beq a0 x0 error26
    mv s9 a0
    lw a0 12(s1)
    mv a1 s8
    mv a2 s9
    jal ra, read_matrix
#     jal ra, randomizeCallerSavedRegsBesidesA0
    mv s10 a0
  
    # Compute h = matmul(m0, input)
    lw t0 0(s3)
    lw t1 0(s8)
    mul a0 t0 t1
    li t0 4
    mul a0 a0 t0
    jal ra, malloc
#     jal ra, randomizeCallerSavedRegsBesidesA0
    beq a0 x0 error26
    mv s11 a0
    
    mv a0 s4
    lw t0 0(s2)
    lw t1 0(s3)
    mv a1 t0
    mv a2 t1
    mv a3 s10
    lw t0 0(s8)
    lw t1 0(s9)
    mv a4 t0
    mv a5 t1
    mv a6 s11
    jal ra, matmul
#     jal ra, randomizeCallerSavedRegsBesidesA0
    
    # Compute h = relu(h)
    mv a0 s11
    lw t0 0(s2)
    lw t1 0(s9)
    mul t0 t0 t1
    mv a1 t0
    jal ra, relu
#     jal ra, randomizeCallerSavedRegsBesidesA0
    
    mv a0 s4
    jal ra, free
    # Compute o = matmul(m1, h)
    lw t0 0(s5)
    lw t1 0(s9)
    mul a0 t0 t1
    li t0 4
    mul a0 a0 t0
    jal ra, malloc
#     jal ra, randomizeCallerSavedRegsBesidesA0
    beq a0 x0 error26
    mv s4 a0
    
    mv a0 s7
    mv a6 s4
    lw t0 0(s5)
    lw t1 0(s6)
    mv a1 t0
    mv a2 t1
    mv a3 s11
    lw t0 0(s2)
    lw t1 0(s9)
    mv a4 t0
    mv a5 t1
    jal ra, matmul
#     jal ra, randomizeCallerSavedRegsBesidesA0
    
    # Write output matrix o
    lw a0 16(s1)
    mv a1 s4
    lw a2 0(s5)
    lw a3 0(s9)
    jal ra, write_matrix
#     jal ra, randomizeCallerSavedRegsBesidesA0
    
    # Compute and return argmax(o)
    mv a0 s4
    lw t0 0(s5)
    lw t1 0(s9)
    mul a1 t0 t1
    jal ra, argmax
#     jal ra, randomizeCallerSavedRegsBesidesA0
    mv s1 a0
    
    # If enabled, print argmax(o) and newline 
    li t0 1
    beq s0 t0 done
    
    jal ra, print_int
    
    li a0 '\n'
    jal ra, print_char
    
done: 
    mv a0 s2
    jal ra, free
    mv a0 s3
    jal ra, free
    mv a0 s5
    jal ra, free
    mv a0 s6
    jal ra, free
    mv a0 s7
    jal ra, free
    mv a0 s8
    jal ra, free
    mv a0 s9
    jal ra, free
    mv a0 s10
    jal ra, free
    mv a0 s4
    jal ra, free
    mv a0 s11
    jal ra, free
    
    ebreak
    mv a0 s1
    lw ra 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    lw s4 16(sp)
    lw s5 20(sp)
    lw s6 24(sp)
    lw s7 28(sp)
    lw s8 32(sp)
    lw s9 36(sp)
    lw s10 40(sp)
    lw s11 44(sp)
    lw s0 48(sp)
    addi sp sp 52
    jr ra
    
    
    
error26:
    li a0, 26
    j exit
    
error31:
    li a0, 31
    j exit