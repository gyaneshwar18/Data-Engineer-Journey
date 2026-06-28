s=input()
chars=list(s)

l=0
r=len(s)-1

while l<r:
    chars[l],chars[r]=chars[r],chars[l]
    l+=1
    r-=1

print("".join(chars))


