import random

def start_game():
    
    mat=[]
    for i in range(4):
        mat.append([0]*4)
    return mat
    
def add_new_2(mat):
    
    # a new two add is added only when some movement is observed,if there is no change after moving then no new 2 is
    # added.
    r=random.randint(0,3) # r and c are some random integers that can take value from 0 to 3 (integers only)
    c=random.randint(0,3)

    while(mat[r][c] != 0):
        r=random.randint(0,3)
        c=random.randint(0,3)
        
    mat[r][c] = 2   
    return mat

                # Whenever you move, you need 3 functions:- 1. Compress 2. Merge 3.Move
def merge(mat):
    
    changed=False
    
    # if any compression or merging happens after a movement than only we add a new 2 in our grid.
    
    for i in range(4):
        for j in range(3):
            if (mat[i][j] == mat[i][j+1] and mat[i][j] != 0):
                mat[i][j] = mat[i][j+1]*2
                mat[i][j+1] = 0
                changed=True
                
    return mat,changed

def compress(mat):
    
    # Here we push 0 values to end in a new matrix and non zeroes value in front in respective order.
    
    changed = False
    new_mat=[]
    for i in range(4):
        new_mat.append([0]*4)
        
    for i in range(4):
        pos=0
        for j in range(4):
            if(mat[i][j] != 0):
                new_mat[i][pos]=mat[i][j]
                
                if j!=pos :    # Just checked for a change here.
                    changed=True
                    
                pos+=1

    return new_mat,changed

# There are two utility functions for moving ,those are : Transpose and Reverse 

def reverse(mat):
    new_mat=[]
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[i][4-j-1])
    return new_mat
    
def transpose(mat):
    new_mat=[]
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[j][i])
    
    return new_mat
                
###### In left move, what happens : compress->Merge->Compress
###### In right move, Reverse->Apply left move->reverse; REVERSING makes a right move similar to left
###### In Up move, Transpose->Apply left move->Transpose    
###### In Down move, Transpose->Apply Right move ->Transpose    

def move_up(grid):
    transposed_grid=transpose(grid)
    new_grid,changed1 = compress(transposed_grid)
    new_grid,changed2 = merge(new_grid)
    changed=changed1 or changed2
    new_grid,temp = compress(new_grid) # temp is of no use,it is just so that returned value can be stored 
    final_grid = transpose(new_grid)
    
    return final_grid,changed

def move_down(grid):
    transposed_grid=transpose(grid)
    reversed_grid = reverse(transposed_grid)
    new_grid,changed1 = compress(reversed_grid)
    new_grid,changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid,temp = compress(new_grid)
    final_reversed_grid = reverse(new_grid)
    final_grid=transpose(final_reversed_grid)

    return final_grid,changed
        

def move_right(grid):
    reversed_grid = reverse(grid)
    new_grid,changed1 = compress(reversed_grid)
    new_grid,changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid,temp = compress(new_grid)
    final_grid = reverse(new_grid)
    
    return final_grid,changed


def move_left(grid):
    new_grid,changed1 = compress(grid)
    new_grid,changed2 = merge(new_grid)
    changed = changed1 or changed2
    final_grid,temp = compress(new_grid)
    
    return final_grid,changed


def get_current_state(mat):
    
    #Three ossible conditions are there ;
    #    1.WON
    #    2.LOST
    #    3.GAME NOT OVER
    
    for i in range(4):
        for j in range(4):
            if(mat[i][j] == 2048):
                return "WON"
            
    for i in range(4):        # If a 0 is present in any block that means that an empty position is present
        for j in range(4):
            if(mat[i][j] == 0):
                return "GAME NOT OVER"
            
    for i in range(3):   # here if consecutive elements either vertically or horizontally present,they can be combined
        for j in range(3): # and more empty positions can be created.Range is take 3 so that index error is taken care
            if(mat[i][j] == mat[i+1][j] or mat[i][j] == mat[i][j+1]):
                return "GAME NOT OVER"
            
    # Now we will see conditions for last row and last column.
    # its a case when now element in 3rd row/column is combinable with 4th row/column respectively.
    
    for j in range(3): # for eg in last row we have 2,2,4,8
        if(mat[3][j] == mat[3][j+1]):
            return  "GAME NOT OVER"
        
    for i in range(3): # for eg in last column we have 4,4,2,8
        if(mat[i][3] == mat[i+1][3]):
            return  "GAME NOT OVER"
    
    return "LOST" #if no conditions is performed that means you Lost the game.


