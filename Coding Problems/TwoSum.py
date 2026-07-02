n = int(input())
nums = list(map(int, input().split()))
target = int(input())

seen = {}

for i in range(n):

    complement = target - nums[i]

    if complement in seen:
        print(seen[complement], i)
        break

    seen[nums[i]] = i