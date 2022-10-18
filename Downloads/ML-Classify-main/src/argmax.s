.globl argmax

.text
# =================================================================
# FUNCTION: Given a int array, return the index of the largest
#   element. If there are multiple, return the one
#   with the smallest index.
# Arguments:
#   a0 (int*) is the pointer to the start of the array
#   a1 (int)  is the # of elements in the array
# Returns:
#   a0 (int)  is the first index of the largest element
# Exceptions:
#   - If the length of the array is less than 1,
#     this function terminates the program with error code 36
# =================================================================
argmax:
    addi sp, sp, -4
    sw ra, 0(sp)
    addi x1, x0, 1
    blt a1, x1, error
 
    li t0, 0 # pos -> 0
    li t4, 4 # sizeofint
    lw t1, 0(a0) # max -> a0[0]
    li t2, 0 # index -> 0

loop_start:
    beq t0, a1, loop_end # pos -> a-1
    mul t3 t4 t0 # offset from original
    add t3 t3 a0
    lw t5 0(t3)
    ble t5 t1 loop_continue
    mv t1 t5
    mv t2 t0
    
loop_continue:
    addi t0 t0 1
    j loop_start

loop_end:
    lw ra, 0(sp)
    addi sp, sp, 4
    mv a0, t2
    ret
 
error:
    li a0 36
    j exit

