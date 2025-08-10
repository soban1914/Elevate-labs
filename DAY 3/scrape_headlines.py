import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def scrape_news_headlines():
    """
    Scrapes news headlines from BBC News website
    Returns a list of headlines
    """
    # URL to scrape - using BBC News as it's reliable and allows scraping
    url = "https://www.bbc.com/news"
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    headlines = []
    
    try:
        print(f"Fetching headlines from: {url}")
        
        # Send GET request to the website
        response = requests.get(url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            print(f"✅ Successfully fetched the webpage (Status: {response.status_code})")
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all headline elements - BBC uses h2 tags with specific classes
            # We'll look for multiple selectors to get more headlines
            headline_selectors = [
                'h2[data-testid="card-headline"]',  # Main headlines
                'h3[data-testid="card-headline"]',  # Secondary headlines
                'h2.sc-4fedabc7-3',  # Alternative selector
                'h3.sc-4fedabc7-3'   # Alternative selector
            ]
            
            for selector in headline_selectors:
                elements = soup.select(selector)
                for element in elements:
                    headline_text = element.get_text(strip=True)
                    if headline_text and headline_text not in headlines:
                        headlines.append(headline_text)
            
            # If the above selectors don't work, try generic h2 and h3 tags
            if not headlines:
                print("Trying alternative selectors...")
                for tag in soup.find_all(['h1', 'h2', 'h3']):
                    headline_text = tag.get_text(strip=True)
                    if headline_text and len(headline_text) > 10:  # Filter out very short text
                        headlines.append(headline_text)
            
            print(f"✅ Found {len(headlines)} headlines")
            
        else:
            print(f"❌ Failed to fetch webpage. Status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching the webpage: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    return headlines

def save_headlines_to_file(headlines, filename="news_headlines.txt"):
    """
    Saves headlines to a text file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            # Write header with timestamp
            file.write(f"NEWS HEADLINES - Scraped on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 60 + "\n\n")
            
            # Write each headline
            for i, headline in enumerate(headlines, 1):
                file.write(f"{i}. {headline}\n\n")
            
            file.write(f"\nTotal Headlines: {len(headlines)}")
        
        print(f"✅ Headlines saved to '{filename}'")
        
    except Exception as e:
        print(f"❌ Error saving to file: {e}")

def main():
    """
    Main function to run the web scraper
    """
    print("🕷️  Starting News Headlines Web Scraper...")
    print("-" * 50)
    
    # Scrape headlines
    headlines = scrape_news_headlines()
    
    if headlines:
        # Display first 5 headlines as preview
        print("\n📰 Preview of scraped headlines:")
        print("-" * 40)
        for i, headline in enumerate(headlines[:5], 1):
            print(f"{i}. {headline}")
        
        if len(headlines) > 5:
            print(f"... and {len(headlines) - 5} more headlines")
        
        # Save to file
        print("\n💾 Saving headlines to file...")
        save_headlines_to_file(headlines)
        
        print("\n🎉 Web scraping completed successfully!")
        
    else:
        print("❌ No headlines were found. The website structure might have changed.")
        print("💡 Try updating the CSS selectors in the code.")

if __name__ == "__main__":
    main()
