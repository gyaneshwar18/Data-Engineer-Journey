import requests
from bs4 import BeautifulSoup
import pandas as pd

URL="https://books.toscrape.com"

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    return response.text

def parse_books(html):
    soup=BeautifulSoup(html,'html.parser')
    books=[]

    for book in soup.select('article.product_pod'):
        title=book.h3.a['title']
        price=book.select_one('p.price_color').text
        rating=book.p['class'][1]  # Get the second class which indicates the rating
        books.append({'Title': title, 'Price': price, 'Rating': rating})
    return books


def save_csv(rows):
    df=pd.DataFrame(rows)
    df.to_csv('books.csv',index=False)  
    print("Data saved to books.csv")

def main():
    print("Fetching page...")
    html=fetch_page(URL)        

    print("Parsing books...")
    books=parse_books(html)

    print("saving to CSV...")
    save_csv(books)
if __name__=="__main__":    
    main()