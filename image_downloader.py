from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time
import re  # Import the regex module for replacing invalid characters

# Set the path to your WebDriver executable
driver_path = "C:/Users/nirivas/Desktop/chromedriver-win64/chromedriver.exe"
url = "https://coralnet.ucsd.edu/image/4016390/view/"

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
# chrome_options.add_argument('--headless')  # Uncomment this line to run headless

# Initialize the Selenium WebDriver using the Service class
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the initial webpage
    driver.get(url)

    # Initialize image counter (you can still track the number of images internally if needed)
    image_counter = 1
    max_images = 1000  # Set the maximum number of images to download

    while image_counter <= max_images:
        # Wait for the page to load and find the image tag
        time.sleep(5)  # Adjust sleep if needed for the page to load
        img_tag = driver.find_element(By.TAG_NAME, 'img')

        # Construct the image URL
        img_url = img_tag.get_attribute('src')

        # Send a GET request to download the image
        img_response = requests.get(img_url)

        # Check if the image request was successful
        if img_response.status_code == 200:
            # Retrieve the custom name "M12_42_0" from the link text
            custom_name = driver.find_element(By.XPATH, "//a[contains(@href,'/image/') and contains(text(),'.jpg')]").text.strip('.jpg')
            
            # Sanitize the custom name by replacing invalid characters
            custom_name = re.sub(r'[\\/*?:"<>|]', "_", custom_name)
            
            # Define the filename and save the image (no image_counter in filename)
            filename = os.path.join(os.getcwd(), f'{custom_name}.jpg')  # No image counter in the filename
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print(f"Image downloaded successfully and saved as {filename}.")
            image_counter += 1
        else:
            print(f"Failed to download image. Status code: {img_response.status_code}")

        # Wait for the "Next" button to be clickable
        try:
            wait = WebDriverWait(driver, 10)  # 10 seconds timeout
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Next')]")))
            next_button.click()
        except Exception as e:
            print("No more images to download or an error occurred:", e)
            break  # Exit the loop if there's no "Next" button

        # Wait for the new page to load
        time.sleep(5)  # You can adjust this if the page takes longer to load

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()

