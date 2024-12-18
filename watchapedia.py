from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
import pandas as pd

# Set up ChromeDriver path
chrome_driver_path = "chromedriver-win64/chromedriver.exe"  # Replace with your ChromeDriver path

# Chrome options to reduce detection risks
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize the driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Target URL
url = "https://pedia.watcha.com/ko-KR/contents/mWyawb6/comments?order=recent"
driver.get(url)
wait = WebDriverWait(driver, 10)

# Lists to store the scraped data
reviews = []
scores = []

# Scroll and extract comments
previous_review_count = 0
scroll_attempts = 0
max_attempts = 10  # Limit to avoid infinite loop

while scroll_attempts < max_attempts:
    try:
        # Wait for the reviews to load
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "A5k28qaV")))

        # Get the review div elements
        review_elements = driver.find_elements(By.CLASS_NAME, "A5k28qaV")

        # Process each review element
        for element in review_elements[previous_review_count:]:  # Only process new reviews
            try:
                # Extract review score
                score = element.find_element(By.CSS_SELECTOR, "div.aytsxOVO span").text

                # Extract review comment
                comment = element.find_element(By.CSS_SELECTOR, "div.eqSewv3p").text

                # Add data to lists
                reviews.append(comment)
                scores.append(score)

                print(f"Scraped Review: {comment[:30]}... | Score: {score}")
            except NoSuchElementException:
                print("Some review elements were not found; skipping.")
                continue

        # Update review count
        new_review_count = len(review_elements)

        if new_review_count == previous_review_count:
            print("No new reviews loaded. Exiting scroll.")
            break

        previous_review_count = new_review_count

        # Scroll down to load more reviews
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)  # Allow content to load
        scroll_attempts = 0  # Reset attempts if successful
    except TimeoutException:
        print("Timeout waiting for reviews. Retrying...")
        scroll_attempts += 1

# Save data to CSV
df = pd.DataFrame({'Review': reviews, 'Score': scores})
df.to_csv("movie_reviews_criminal_city4.csv", index=False, encoding='utf-8-sig')

print("Data saved to movie_reviews_criminal_city4.csv")

# Close the driver
driver.quit()
