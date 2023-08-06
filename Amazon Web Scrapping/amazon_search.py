from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os

# Get the path to the current directory and chromedriver.exe
current_directory = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(current_directory, 'chromedriver.exe')

# Launch the Chrome browser using webdriver and specify the chromedriver path
driver = webdriver.Chrome(executable_path=chromedriver_path)

amazon_url = "https://www.amazon.com/s?k=gaming+laptop"

# Set the maximum number of pages to scrape (adjust as needed)
max_pages = 5

# Set the number of results per page to scrape (adjust as needed)
results_per_page = 10

product_data = []

for page in range(1, max_pages + 1):
    page_url = f"{amazon_url}&page={page}"
    # Load the page using webdriver
    driver.get(page_url)

    # Wait for the page to load and dynamic content to populate (adjust the time as needed)
    driver.implicitly_wait(10)

    # Get the page source after dynamic content has loaded
    page_source = driver.page_source

    # Use BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all product containers
    product_containers = soup.select('div[data-component-type="s-search-result"]')
    for container in product_containers:
        title_element = container.select_one('span.a-size-medium')
        price_element = container.select_one('span.a-offscreen')
        product_url_element = container.select_one('a.a-link-normal')
        image_url_element = container.select_one('img[srcset]')
        rating_element = container.select_one('span.a-icon-alt')

        title = title_element.text.strip() if title_element else 'N/A'
        price = price_element.text.strip() if price_element else 'N/A'
        product_url = "https://www.amazon.com" + product_url_element['href'] if product_url_element else 'N/A'
        image_url = image_url_element['srcset'].split(',')[0].strip() if image_url_element else 'N/A'
        rating = rating_element.text.strip() if rating_element else 'N/A'

        # Extract the brand name from the title
        brand = title.split(' ')[0] if title else 'N/A'

        product_data.append({
            'Title': title,
            'Price': price,
            'ProductURL': product_url,
            'ImageURL': image_url,
            'Brand': brand,
            'Rating': rating
        })

# Close the browser
driver.quit()

# Save the data to a JSON file
with open('amazon-search.json', 'w', encoding='utf-8') as file:
    json.dump(product_data, file, ensure_ascii=False, indent=2)