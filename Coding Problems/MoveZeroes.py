n = int(input())
nums = list(map(int, input().split()))

j = 0

for i in range(n):
    if nums[i] != 0:
        nums[j], nums[i] = nums[i], nums[j]
        j += 1

print(*nums)