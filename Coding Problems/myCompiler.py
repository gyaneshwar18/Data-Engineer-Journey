n = int(input())
ar = list(map(int, input().split()))

max_ele = ar[0]

for i in ar:
    if i > max_ele:
        max_ele = i

print(max_ele)