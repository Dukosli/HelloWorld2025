





# From G4G, change to sort by k-d depth
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

    # Copy the remaining elements of L[],
    # if there are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], 
    # if there are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSort(arr, left, right):
    if left < right:
        mid = (left + right) // 2

        mergeSort(arr, left, mid)
        mergeSort(arr, mid + 1, right)
        merge(arr, left, mid, right)
        
def sortByDepth(dict_in, temp, depth):
    temp = [0] * len(dict_in)
    i = 0
    
    for key, value in dict_in.items():
        temp[i] = [key, value[depth]]
        i += 1
        
    mergeSort(temp, 0, len(temp) - 1)
    for i in temp:
        print(i)
    
newDict = {
    1:[1,2,3],
    3:[5,4,2],
    2:[10,1,1] }

tempor = []
sortByDepth(newDict, tempor, 2)
for i in tempor:
    print(i[0] + " ")