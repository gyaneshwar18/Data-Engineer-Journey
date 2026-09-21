n=int(input())
words=input().split()

freq={}

for word in words:
    key=''.join(sorted(word))

    if key not in freq:
          freq[key]=[]
    freq[key].append(word)

print(list(freq()))