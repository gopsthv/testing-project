import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.skillrack.com/")  # Replace with your target website
time.sleep(3)  

# Take an initial screenshot
driver.save_screenshot("before_check.png")
print("Screenshot of the page saved: before_check.png")

# Find all links on the page
links = driver.find_elements(By.TAG_NAME, "a")

# Open a log file to store results
broken_found = False  # Track if broken links exist
with open("broken_links_log.txt", "w", encoding="utf-8") as log_file:
    for link in links:
        url = link.get_attribute("href")
        if url:
            try:
                response = requests.head(url, allow_redirects=True)
                if response.status_code >= 400:
                    print(f"Broken link found: {url} (Status: {response.status_code})")
                    log_file.write(f"Broken link found: {url} (Status: {response.status_code})\n")
                    broken_found = True  # Set flag to true
                    
                    # Take a screenshot when a broken link is found
                    driver.save_screenshot("broken_link_screenshot.png")
                    print("Screenshot saved: broken_link_screenshot.png")

                else:
                    print(f"Link is working: {url}")
                    log_file.write(f"Link is working: {url}\n")
                    
            except requests.exceptions.RequestException:
                print(f"Error accessing: {url}")
                log_file.write(f"Error accessing: {url}\n")

# If no broken links were found, save a final screenshot
if not broken_found:
    driver.save_screenshot("final_page.png")
    print(" Screenshot of the final page saved: final_page.png")

# Close the browser
driver.quit()
print("Check completed. Results saved in 'broken_links_log.txt'")


