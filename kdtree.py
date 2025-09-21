import heapq as hq
import numpy as np
# import time

# Organization
class Node:
    def __init__(self, i_key, v_val, depth):
        self.id = i_key
        self.point = v_val
        self.axis = depth
        self.left = None
        self.right = None
        
def newNode(in_key, vec_val, d):
    return Node(in_key, vec_val, d)

# INPUT FORMAT:

# Add nodes from dict format:
# data_dict = {
#     movie_1_id: [rating_value, genre_1_val, genre_2_val, etc.],
#     movie_2_id: [rating_value, genre_1_val, genre_2_val, etc.],
#     ...
# }
# Then, output list in form:
# [[movie_1_id, vector], [movie_2_id, vector], ...]
# Exclusively access points from index 1 of each list_out item
def addNodes(dict_in, list_out):
    for key, value in dict_in.items():
        # Value is the vector
        list_out.append(newNode(key, value, None))
        
# def getMovieByID(id_name_dict, iD):
#     return id_name_dict[iD]
        
# Expect Node[], int input
def buildTree(points, depth):
    # Check if points is empty
    # Return the default leaf setting
    if not points:
        return None
    
    # Gets current "depth" values, like which axis we are on
    k = len(points[0].point)
    c_dim = depth % k
    
    # Expects Node[], int
    sortByDepth(points, c_dim)
    
    median_ind = len(points) // 2
    median_point = points[median_ind]
    median_point.axis = c_dim
    
    # Recursively builds the left and right nodes
    median_point.left  = buildTree(points[:median_ind], depth + 1)
    median_point.right = buildTree(points[median_ind + 1:], depth + 1)
    
    return median_point

# Expects node, vector
def getDistanceNQ(node, query):
    dist = np.linalg.norm(np.array(node.point) - np.array(query))
    return dist

# Root is the start node, returned from buildTree
# Query is the input vector, k is the number of returns
# Invert the heap so furthest distance is also smallest number
def kNearestNeighbors(node, query, k, heap):
    if not node:
        return
    
    # Get distance with numpy
    dist = getDistanceNQ(node, query)

    if len(heap) < k:
        hq.heappush(heap, (-dist, node))
    else:
        if dist < -heap[0][0]:  # compare to farthest
            hq.heapreplace(heap, (-dist, node))
            
    # Compare along the splitting axis since during the generation
    # phase, we checked by axis. This way, we know which branch is
    # closer on that seperation. 
    axis = node.axis
    diff = query[axis] - node.point[axis]
    
    near_branch = node.left if diff < 0 else node.right
    far_branch  = node.right if diff < 0 else node.left
        
    kNearestNeighbors(near_branch, query, k, heap)
    
    # Far branch mathematical condition to satisfy:
    # 
    if len(heap) < k or abs(diff) < -heap[0][0]:
        kNearestNeighbors(far_branch, query, k, heap)


# ------------------------------- MERGESORT ------------------------------- #

# Below contains mergesort, pulled from G4G, with 
# slight modification to the deployment to re-configure 
# the array to be suitable for batch structurization
# in the k-d tree rather than by-point insert.


# From G4G, change to sort by k-d depth at 
# level to find median by dimension at every level
def merge(arr, left, mid, right, axis):
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
        if L[i].point[axis] <= R[j].point[axis]:
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
def mergeSort(arr, left, right, axis):
    if left < right:
        mid = (left + right) // 2

        mergeSort(arr, left, mid, axis)
        mergeSort(arr, mid + 1, right, axis)
        merge(arr, left, mid, right, axis)
        
# Sort by depth, temp changes as passed by
def sortByDepth(node_in, depth):
    mergeSort(node_in, 0, len(node_in) - 1, depth)


# ------------------------------- PRIMARY FUNCTIONALITY ------------------------------- #

def rknn_id(dict_in, query, k):
    # start_time = time.time();
    
    # Convert input dictionary to Node[]
    nams = []
    addNodes(dict_in, nams)
    
    # Build k-d tree with root as base
    root = buildTree(nams, 0)
    
    # Get nearest neighbors through heap return
    heap = []
    kNearestNeighbors(root, query, k, heap)
    
    # Interpret heap data to sort into list of IDs
    sorted_neighbors = sorted(heap, key=lambda x: -x[0])
    neighbor_ids = [node.id for dist, node in sorted_neighbors]
    
    # end_time = time.time()
    # execution_time = end_time-start_time
    # print(execution_time)
    
    return neighbor_ids

# ------------------------------- TESTING GROUNDS ------------------------------- #

# nodes = []
# nodes.append(newNode(1, [1,2]))
# nodes.append(newNode(2, [10,3]))
# nodes.append(newNode(3, [5,4]))

# sortByDepth(nodes, 1)
# for i in nodes:
#     print(i.id, i.point)

# # Chat-generated test cases
# data_dict = {
#   1: [8.44, 6.25, 2.10],
#   2: [1.32, 9.87, 5.76],
#   3: [4.91, 3.45, 7.80],
#   4: [9.65, 0.55, 1.10],
#   5: [2.34, 6.78, 9.01],
#   6: [7.12, 8.90, 4.56],
#   7: [5.67, 2.22, 3.33],
#   8: [3.11, 7.77, 0.99]
# }
# queries = [
#     [8.0,6.0,2.0],
#     [2.0,7.0,8.0],
#     [5.5,2.0,3.0],
#     [3.0,8.0,1.0],
#     [9.0,1.0,1.0]
# ]

# nams = []
# addNodes(data_dict, nams)
# root = buildTree(nams, 0)

# # Chat generated print-assist
# def printTree(node, depth=0):
#     if node is None:
#         return
#     print("  " * depth + f"ID={node.id}, Point={node.point}, Depth={node.axis}")
#     printTree(node.left, depth + 1)
#     printTree(node.right, depth + 1)

# # Print the constructed tree
# printTree(root)


# # Expect 1, 5, 7, 8, 4
# for q in queries:
#     print(f"Query {q} -> Nearest ID: {rknn_id(data_dict, q, 2)}")