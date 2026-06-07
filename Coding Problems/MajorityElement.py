# class Solution:
#     def majorityElement(self, nums: List[int]) -> int:

#         counter = {}

#         for num in nums:
#             if num in counter:
#                 counter[num] += 1
#             else:
#                 counter[num] = 1

#         max_count = -1
#         ans = -1

#         for key, val in counter.items():
#             if val > max_count:
#                 max_count = val
#                 ans = key

#         return ans

n = int(input())
nums = list(map(int, input().split()))

freq = {}

for num in nums:
    freq[num] = freq.get(num, 0) + 1

for key, value in freq.items():
    if value > n // 2:
        print(key)
        break