import sys

# Most important variable in the tree, indicates
# max dimensionality of the k-d tree
univDepth = 1

class Node:
    def __init__(self, i_key, v_val):
        self.id = i_key
        self.point = v_val
        self.left = None
        self.right = None
        
def newNode(in_key, vec_val):
    return Node(in_key, vec_val)

# Add nodes from dict format:
# data_dict = {
#     movie_1_id: [rating_value, genre_1_val, genre_2_val, etc.],
#     movie_2_id: [rating_value, genre_1_val, genre_2_val, etc.],
#     ...
# }
# Then, output list in form:
# [[movie_1_id, vector], [movie_2_id, vector], ...]
def addNodes(dict_in, list_out):
    for key, value in dict_in.items():
        list_out.append(newNode(key, value))






# ------------------------------- MERGESORT ------------------------------- #

# Below contains mergesort, pulled from G4G, with 
# slight modification to the deployment to re-configure 
# the array to be suitable for batch structurization
# in the k-d tree rather than by-point insert.


# From G4G, change to sort by k-d depth at 
# level to find median by dimension at every level
def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    # Create temp arrays
    L = [0] * n1
    R = [0] * n2

    # Copy data to temp arrays L[] and R[]
    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]
        
    i = 0  
    j = 0  
    k = left  

    # Merge the temp arrays back
    # into arr[left..right]
    while i < n1 and j < n2:
        if L[i][1] <= R[j][1]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Dump remainder after comparison burns
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

# Head
def mergeSort(arr, left, right):
    if left < right:
        mid = (left + right) // 2

        mergeSort(arr, left, mid)
        mergeSort(arr, mid + 1, right)
        merge(arr, left, mid, right)
        
# Sort by depth, temp changes as passed by
def sortByDepth(dict_in, temp, depth):
    temp.clear()
    
    for key, value in dict_in.items():
        temp.append([key, value[depth]])
        
    mergeSort(temp, 0, len(temp) - 1)
    
# ------------------------------- MERGESORT ------------------------------- #