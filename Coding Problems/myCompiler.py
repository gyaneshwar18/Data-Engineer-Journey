n=int(input())
ar = list(map(int, input().split()))

freq={}

for num in ar:
    if num in freq:
        freq[num]+=1
    else:
        freq[num]=1

for key, value in freq.items():
    if value>1:
        print("true")
        break
else:
    print("false")
        
