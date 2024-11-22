import requests
from bs4 import BeautifulSoup
import csv
import time

def extract_article_details(article):
    try:
        title = article.find("h3").get_text(strip=True)
    except AttributeError:
        title = None

    try:
        link = article.find("a")["href"]
        if not link.startswith("http"):
            link = "https://www.kaspr.io" + link
    except (AttributeError, TypeError):
        link = None

    try:
        summary = article.find("p").get_text(strip=True)
    except AttributeError:
        summary = None

    return {
        "Title": title,
        "Link": link,
        "Summary": summary,
    }

def scrape_blog_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during HTTP request: {e}")
        return []
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("div", class_="blog-article")
    return [extract_article_details(article) for article in articles]

def main():
    base_url = "https://www.kaspr.io/blog/b2b-contact-database"
    data = []
    for page in range(1, 4):
        print(f"Scraping page {page}...")
        url = f"{base_url}?page={page}"
        page_data = scrape_blog_page(url)
        if not page_data:
            print("No more articles found or an error occurred.")
            break
        data.extend(page_data)
        time.sleep(2)
    with open("kaspr_blog_articles.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Link", "Summary"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Scraping completed. {len(data)} articles saved to 'kaspr_blog_articles.csv'.")

if __name__ == "__main__":
    main()
