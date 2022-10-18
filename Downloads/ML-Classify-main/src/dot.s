.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int arrays
# Arguments:
#   a0 (int*) is the pointer to the start of arr0
#   a1 (int*) is the pointer to the start of arr1
#   a2 (int)  is the number of elements to use
#   a3 (int)  is the stride of arr0
#   a4 (int)  is the stride of arr1
# Returns:
#   a0 (int)  is the dot product of arr0 and arr1
# Exceptions:
#   - If the length of the array is less than 1,
#     this function terminates the program with error code 36
#   - If the stride of either array is less than 1,
#     this function terminates the program with error code 37
# =======================================================
dot:
    
    addi sp, sp, -16
    sw ra 0(sp)
    sw t4 4(sp)
    sw x3 8(sp)
    sw t1 12(sp)
    
    li t0 1
    
    blt a2 t0 exit36
    blt a3 t0 exit37
    blt a4 t0 exit37
    
    add t1 x0 a0 # pos1 -> 0
    add t2 x0 a1 # pos2 -> 0
    
    li x5 4
    mul t5 a3 x5
    mul t6 a4 x5
    mv t0, a0   
    add x1 x0 x0
    li x3 0 # count ->
    
loop_start:
    beq x3 a2 loop_end
    lw t3 0(t1)
    lw t4 0(t2)
    mul x4 t3 t4
    add x1 x1 x4
    add t1 t1 t5
    add t2 t2 t6
    addi x3, x3, 1
    j loop_start
     
loop_end:
    add a0, x0, x1
    lw ra 0(sp)
    lw t4 4(sp)
    lw x3 8(sp)
    lw t1 12(sp)
    addi sp, sp, 16

    ret
 
exit36:
    addi sp, sp, 12
    li a0 36
    j exit

exit37:
    addi sp, sp, 12
    li a0 37
    j exit
