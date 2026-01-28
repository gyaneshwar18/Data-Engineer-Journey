#word_counter

def word_counter(text):
    word=text.split()
    word_len=len(word)
    char_len=len(text.replace(" ","")) #character len
   
    
    frequency={}
    for w in word:
        w=w.lower().strip(",.!?")    
         # frequency[w]=frequency.get(w,0)+1  
        if w not in frequency:    
            frequency[w]=0
        frequency[w]+=1
    return char_len, word_len,frequency

# if __name__=="__main__":
#     text=input("Enter name: ")
#     word_len, char_len,frequency=word_counter(text)
#     print(f"\nTotal words:{word_len}")
#     print(f"\nCharacter length:{char_len}")
#     print(frequency)
