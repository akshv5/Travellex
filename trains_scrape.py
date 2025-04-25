from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup
import time
import json  # Import the json library
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Set up Edge options
edge_options = EdgeOptions()
#edge_options.add_argument("--headless=new")
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--force-device-scale-factor=1")
# Path to your Edge WebDriver executable
edge_driver_path = "D:/msedgedriver.exe"

# Initialize the Edge service and driver
try:
    service = EdgeService(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)

except Exception as e:
    print(f"Error initializing Edge driver: {e}")
    print("Make sure you have the correct msedgedriver.exe and its in the right location.  It also must be compatible with the Edge browser version.")
    exit()

# URL of the ixigo train search results page
url = "https://www.ixigo.com/search/result/train/LKO/CSMT/17042025//1/0/0/0/ALL"

trains_data = []  # Initialize an empty list to store train data

try:
    # Load the page
    driver.get(url)
    time.sleep(5)
    # Wait for the page to load dynamically
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "train-listing-row"))
        )
        print("Train listings loaded.")
    except TimeoutException:
        print("Timed out waiting for train listings to load.")
        driver.quit()
        exit()

    # Get the page source after dynamic content has loaded
    html = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all train listing rows
    train_listings = soup.find_all('li')

    # Iterate through the train listings and extract data
    for train_listing in train_listings:
        try:
            train_number = train_listing.find('span', class_='train-number').text
            train_name = train_listing.find('span', class_='train-name').text
            origin_station = train_listing.find('div', class_='left-wing').find('a').text
            destination_station = train_listing.find('div', class_='right-wing').find('a').text
            departure_time = train_listing.find('div', class_='left-wing').find('div', class_='time').text
            arrival_time = train_listing.find('div', class_='right-wing').find('div', class_='time').text

            train_data = {  # Create a dictionary for each train
                'train_number': train_number,
                'train_name': train_name,
                'origin_station': origin_station,
                'destination_station': destination_station,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'classes': []  # Initialize an empty list for classes within the train
            }

            # Find available classes and their fares
            train_class_wrapper = train_listing.find('div', class_='train-class-wrapper')
            if train_class_wrapper:
                train_classes = train_class_wrapper.find_all('div', class_='train-class-item')
                for train_class in train_classes:
                    class_name = train_class.find('span', class_='train-class').text
                    try:
                        fare = train_class.find('span', class_='').text
                    except:
                        fare = "NA"

                    availability_class = train_class.find('div', class_='avail-class').text

                    class_data = {  # Create a dictionary for each class
                        'class_name': class_name,
                        'fare': fare,
                        'availability': availability_class
                    }
                    train_data['classes'].append(class_data)  # Append the class data to the train's classes list

            trains_data.append(train_data)  # Append the train data to the overall list
            print(f"Extracted {train_name} and appending")


        except Exception as e:
            print(f"Error extracting data from a train listing: {e}")
            pass

except Exception as e:
    print(f"Error during web scraping: {e}")

# finally:
#     # Close the browser window
#     driver.quit()

# Write the data to a JSON file
try:
    with open("trains_data.json", "w", encoding='utf-8') as f:
        json.dump(trains_data, f, indent=4, ensure_ascii=False)  # Use indent for pretty formatting and ensure_ascii=False for unicode

    print("Data saved to trains_data.json")

except Exception as e:
    print(f"Error saving data to JSON file: {e}")