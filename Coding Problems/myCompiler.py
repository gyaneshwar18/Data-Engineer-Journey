s= input()
t= input()


freq1={}
freq2={}
for ch in s:

    if ch in freq1:
        freq1[ch]+=1
    else:
        freq1[ch]=1 

for ch in t:

    if ch in freq2:
        freq2[ch]+=1
    else:
        freq2[ch]=1 


print(freq1==freq2)