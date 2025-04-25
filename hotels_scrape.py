from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
import time
import json
from urllib.parse import urlencode

def get_hotel_details(location_id, location_name, checkin_date, checkout_date, adult_count, room_count, child_count, msedgedriver_path='msedgedriver.exe', headless=False):
    """
    Extracts hotel details from ixigo.com for the given parameters.

    Args:
        location_id (int): The location ID.
        location_name (str): The location name.
        checkin_date (str): The check-in date (DDMMYYYY).
        checkout_date (str): The check-out date (DDMMYYYY).
        adult_count (int): The number of adults.
        room_count (int): The number of rooms.
        child_count (int): The number of children.
        msedgedriver_path (str): Path to the msedgedriver executable.
        headless (bool): Run the browser in headless mode (no GUI).

    Returns:
        list: A list of dictionaries, where each dictionary contains the details of a hotel.
    """

    # Set up Edge WebDriver
    edge_options = EdgeOptions()
    edge_options.add_argument("--start-maximized")  # Start the browser maximized
    edge_options.add_argument("--force-device-scale-factor=1")  # Set the device scale factor
    if headless:
        edge_options.add_argument("--headless=new")  # Run in headless mode (no browser window)
    edge_service = EdgeService(executable_path=msedgedriver_path)
    driver = webdriver.Edge(service=edge_service, options=edge_options)

    # Construct the URL using parameters
    base_url = "https://www.ixigo.com/hotels/search/result?"
    params = {
        "locationId": location_id,
        "locationName": location_name,
        "locationType": "S",  # This is likely constant
        "masterLocationId": 48569, #This is likely constant
        "countryId": 1, #This is likely constant
        "checkinDate": checkin_date,
        "checkoutDate": checkout_date,
        "adultCount": adult_count,
        "roomCount": room_count,
        "childCount": child_count,
        "ab": "HOTELS-SEARCH-AB-2__variant-B"  # This is likely constant
    }
    url = "https://www.ixigo.com/hotels/search/result?locationId=982&locationName=Mumbai&locationType=C&masterLocationId=49654&countryId=1&checkinDate=17042025&checkoutDate=22042025&adultCount=2&roomCount=1&childCount=0&ab=HOTELS-SEARCH-AB-2__variant-B&source=flight%20search%20bundle&subsource="

    driver.get(url)

    time.sleep(5)
    # Function to scroll to the bottom of the page
    def scroll_to_bottom():
        old_position = 0
        new_position = None

        while new_position != old_position:
            old_position = driver.execute_script(
                ("return (document.documentElement.scrollHeight || document.body.scrollHeight);"))
            driver.execute_script((
                "window.scrollTo(0, document.documentElement.scrollHeight || document.body.scrollHeight);"
            ))
            time.sleep(3)
            new_position = driver.execute_script(
                ("return (document.documentElement.scrollHeight || document.body.scrollHeight);"))

    # Scroll to the bottom of the page to load all content
    scroll_to_bottom()

    # Find all hotel card elements
    hotel_cards = driver.find_elements(By.XPATH, "//a[@target='_blank' and @rel='nofollow']")
    print(len(hotel_cards))
    
    # Extract hotel details from each card
    hotel_data = []
    for card in hotel_cards:
        try:
            hotel_name = card.find_element(By.XPATH, ".//h2[@data-testid='hotel-name']").text
            location = card.find_element(By.XPATH, ".//p[@class='body-sm word-break   break-words text-secondary']").text
            try:
                rating = card.find_element(By.XPATH, ".//div[@class='flex items-center justify-center rounded-5 bg-inverse mr-10']/p").text
                num_ratings = card.find_element(By.XPATH, ".//p[@class='body-sm  text-secondary font-normal']").text
            except:
                rating = "N/A"
                num_ratings = "N/A"
            price = card.find_element(By.XPATH, ".//div[@class='h5 text-right text-primary font-medium']").text
            offering = [off.text for off in card.find_elements(By.XPATH, ".//p[@data-testid='offering']")]
            link = card.get_attribute("href")

            try:
                discount= card.find_element(By.XPATH, ".//div[@class='bg-success-subtle text-success-subtle border-success-subtle min-h-30px icon-md body-sm inline-flex items-center font-normal rounded-full px-1 border border-solid mb-5']/span").text
            except:
                discount = "N/A"

            try:
                original_price = card.find_element(By.XPATH, ".//p[@class='body-xs mr-5  line-through decoration-neutral-600 text-secondary']").text
            except:
                original_price = "N/A"

            # Extract stars (number of star icons)
            stars = len(card.find_elements(By.XPATH, ".//svg[@data-testid='starActive']"))

             #Extract images src
            images = [img.get_attribute('src') for img in card.find_elements(By.XPATH,".//img[@loading='eager']")]

            try:
                taxes = card.find_element(By.XPATH, ".//p[@class='body-xs  text-secondary']").text
            except:
                taxes = "N/A"

            hotel_info = {
                "name": hotel_name,
                "location": location,
                "rating": rating,
                "number_of_ratings": num_ratings,
                "price": price,
                "offering": offering,
                "link": link,
                "discount": discount,
                "original_price": original_price,
                "stars": stars,
                "images": images,
                "taxes": taxes,
                "per_night_per_room": "per night, per room"
            }
            hotel_data.append(hotel_info)

        except Exception as e:
            print(f"Error extracting data from a card: {e}")

    # driver.quit()
    return hotel_data


# Example usage
location_id = 32
location_name = "Mumbai"
checkin_date = "17042025"
checkout_date = "22042025"
adult_count = 2
room_count = 1
child_count = 0
msedgedriver_path = 'D:/msedgedriver.exe'  # Replace with the actual path to your msedgedriver.exe
headless = False # set True to run without browser

hotel_details = get_hotel_details(location_id, location_name, checkin_date, checkout_date, adult_count, room_count, child_count, msedgedriver_path, headless)

# Save the hotel data to a JSON file
filename = "ixigo_hotel_details.json"
try:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(hotel_details, f, indent=4)
    print(f"Hotel details saved to {filename}")
except Exception as e:
    print(f"Error saving to JSON: {e}")