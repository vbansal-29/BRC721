.globl relu

.text
# ==============================================================================
# FUNCTION: Performs an inplace element-wise ReLU on an array of ints
# Arguments:
#   a0 (int*) is the pointer to the array
#   a1 (int)  is the # of elements in the array
# Returns:
#   None
# Exceptions:
#   - If the length of the array is less than 1,
#     this function terminates the program with error code 36
# ==============================================================================
relu:
    addi sp, sp, -4
    sw ra, 0(sp)

    li x1, 1
    blt a1, x1, error
    
    li t1, 0
    li t2, 4
    
loop:
    beq a1, t1, loop_end
    mul t4, t1, t2
    add t4, t4, a0
    lw t3, 0(t4)
    bgt t3, x0, loop_continue
    sub t3, t3, t3
    sw t3, 0(t4)
    
loop_continue:
    addi t1, t1, 1
    j loop

loop_end:
    lw ra, 0(sp)
    addi sp, sp, 4
    ret

error:
    li a0 36
    j exit
