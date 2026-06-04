n = int(input())
arr = list(map(int, input().split()))

is_sorted = True

for i in range(n - 1):
    if arr[i] > arr[i + 1]:
        is_sorted = False
        break

print(is_sorted)