s=input()

l=0
r=len(s)-1

while l<r:

    while l<r and not s[l].isalnum():
        l+=1

    while l<r and not s[r].isalnum():
        r-=1

    while s[l].lower()!=s[r].lower()
        print(False)
        break

    l += 1
    r -= 1

else:
    print(True)


    

