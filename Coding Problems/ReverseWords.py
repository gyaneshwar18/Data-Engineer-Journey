n=input()
ar=list(map(input().split()))

l=0
r=n-1

for l in ar:
    ar[l],ar[r]=ar[r],ar[l]
    l+=1
    r-=1

print(ar)
