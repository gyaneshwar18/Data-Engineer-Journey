s = input()

freq = {}

# Count frequencies
for ch in s:
    freq[ch] = freq.get(ch, 0) + 1

# Find first unique character
for i in range(len(s)):
    if freq[s[i]] == 1:
        print(i)
        break
else:
    print(-1)