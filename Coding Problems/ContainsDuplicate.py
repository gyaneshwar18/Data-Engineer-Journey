#using HashMap

# n = int(input())
# nums = list(map(int, input().split()))

# freq = {}

# for num in nums:
#     freq[num] = freq.get(num, 0) + 1

# for value in freq.values():
#     if value > 1: 
#         print(True)
#         break
# else:
#     print(False)

#using set

n = int(input())
nums = list(map(int, input().split()))

seen = set()

for num in nums:

    if num in seen:
        print(True)
        break

    seen.add(num)

else:
    print(False)



