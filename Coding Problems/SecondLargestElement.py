n = int(input())
arr = list(map(int, input().split()))

largest = float('-inf')
second_largest = float('-inf')

for num in arr:

    if num > largest:
        second_largest = largest
        largest = num

    elif num > second_largest and num != largest:
        second_largest = num

if second_largest == float('-inf'):
    print(-1)
else:
    print(second_largest)