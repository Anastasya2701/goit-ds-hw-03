import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def scrape_quotes():
    quotes_data = []
    authors_data = {}
    
    page = 1
    while True:
        soup = get_soup(f"{BASE_URL}/page/{page}/")
        quotes = soup.find_all("div", class_="quote")
        
        if not quotes:
            break
        
        for quote in quotes:
            text = quote.find("span", class_="text").get_text()
            author_name = quote.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            
            quotes_data.append({
                "quote": text,
                "author": author_name,
                "tags": tags
            })
            
            if author_name not in authors_data:
                author_url = BASE_URL + quote.find("a")["href"]
                author_soup = get_soup(author_url)
                
                fullname = author_soup.find("h3", class_="author-title").get_text().strip()
                born_date = author_soup.find("span", class_="author-born-date").get_text()
                born_location = author_soup.find("span", class_="author-born-location").get_text().strip("in ")
                description = author_soup.find("div", class_="author-description").get_text().strip()
                
                authors_data[author_name] = {
                    "fullname": fullname,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                }
        
        page += 1
    
    return quotes_data, authors_data

def save_data(quotes, authors):
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)
    
    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    quotes, authors = scrape_quotes()
    save_data(quotes, authors)
    print("Скрапінг завершено та дані збережено у файли quotes.json і authors.json.")