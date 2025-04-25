import json
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from urllib.parse import quote
from bs4 import BeautifulSoup  # Import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import deque



edge_driver_path = r"D:\msedgedriver.exe"  # Replace with your path
edge_options = EdgeOptions()
#edge_options.add_argument("--headless=new")  # Uncomment for headless mode
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--force-device-scale-factor=0.05")
edge_service = EdgeService(executable_path=edge_driver_path)
driver = webdriver.Edge(service=edge_service, options=edge_options)


def access_ixigo(from_city="LKO", to_city="BOM",
                 date="17042025", return_date="22042025",
                 adults=2, children=0, infants=0, flight_class="e",
                 hbs=True):
    """
    Accesses the Ixigo flight search website and extracts flight information
    *including* structured data extracted from the HTML of each flight card.

    Args:
        from_city (str): Departure city code.
        to_city (str): Destination city code.
        date (str): Departure date (DDMMYYYY).
        return_date (str): Return date (DDMMYYYY).
        adults (int): Number of adults.
        children (int): Number of children.
        infants (int): Number of infants.
        flight_class (str): Flight class (e.g., "e" for economy).
        hbs (bool): Whether to search for hotel-bundled savings.
    """

    # Construct the URL (using f-strings for readability)
    base_url = "https://www.ixigo.com/search/result/flight"
    params = {
        "from": from_city,
        "to": to_city,
        "date": date,
        "returnDate": return_date,
        "adults": adults,
        "children": children,
        "infants": infants,
        "class": flight_class,
        "source": "Search+Form",  # Note: The space is encoded as '+'
        "hbs": str(hbs).lower()  # Convert boolean to lowercase string
    }

    # Build the query string
    query_string = "&".join([f"{key}={quote(str(value))}" for key, value in params.items()])  # use quote to encode spaces and special characters
    url = f"{base_url}?{query_string}"

    try:
        driver.get(url)
        time.sleep(5)  # Allow time for page to load and flights to populate
        

        print("Page Title:", driver.title)

        flight_data = extract_ixigo_flight_data(driver)

        # with open("ixigo_flights.json", "w", encoding="utf-8") as f:
        #     json.dump(flight_data, f, indent=4, ensure_ascii=False)

        print("Flight data saved to ixigo_flights.json")

    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
        #driver.quit()  # Ensure the driver quits, especially after an error


def extract_ixigo_flight_data(driver):
    """
    Extracts flight data from the Ixigo search results page,
    extracting both structured data and using BeautifulSoup to parse the HTML.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        A list of dictionaries, where each dictionary represents a flight.
    """
    # WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="shadow-[0px_2px_5px_0px_rgba(0,0,0,0.10)] p-15 mb-20  rounded-10 relative cursor-pointer bg-white border border-white transition-all duration-300 ease-in hover:scale-[1.01] hover:shadow-300 hover:duration-300 hover:ease-out"]'))
    #     )

    flight_data = []  # Use deque for efficient appending
    flight_cards_data = []
    flight_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer')]")
    # for  flight_card in flight_cards:
    #     print(flight_card)
    print(len(flight_cards))
    for card in flight_cards:
        try:
            # **Scroll to the element before extracting**
            # driver.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(0.5)  # Give it a brief pause to fully load after scrolling

            # **Extract the HTML**
            html_string = card.get_attribute('outerHTML')

            # **Parse the HTML with BeautifulSoup**
            flight = extract_flight_data_from_html(html_string)  # Use the parsing function

            flight_data.append(flight)

        except Exception as e:
            print(f"Error extracting data from a flight card: {e}")
            continue

    return flight_data


def extract_flight_data_from_html(html_string):
    """
    Extracts specific flight data from the HTML of a flight card using BeautifulSoup.
    This function extracts:
    - Fastest flight indicator
    - Airline
    - Departure Time
    - Arrival Time
    - Flight Duration
    - Stops
    - Price
    """
    soup = BeautifulSoup(html_string, 'html.parser')

    flight = {}

    # Fastest flight indicator
    fastest_element = soup.find('div', class_='text-selection-outline border-selection-outline min-h-20 icon-sm body-xs inline-flex items-center font-normal rounded-full px-px border border-solid bg-white')
    flight['fastest'] = True if fastest_element else False

    # Airline
    airline_element = soup.find('p', class_='body-sm body-sm')
    flight['airline'] = airline_element.text.strip() if airline_element else None

    # Departure Time
    departure_time_element = soup.find('h5', class_='h5 text-primary font-medium')
    flight['departure_time'] = departure_time_element.text.strip() if departure_time_element else None

    # Arrival Time (look for the element with GOX as destination which is now generic GOI)
    arrival_time_element = soup.find_all('h5', class_='h5 text-primary font-medium')[1]
    flight['arrival_time'] = arrival_time_element.text.strip() if len(soup.find_all('h5', class_='h5 text-primary font-medium')) > 1 and arrival_time_element else None #get the second element

    # Flight Duration
    duration_element = soup.find('p', class_='body-sm text-secondary')
    flight['duration'] = duration_element.text.strip() if duration_element else None

    # Stops
    stops_element = soup.find_all('p', class_='body-sm text-secondary')
    flight['stops'] = stops_element[1].text.strip() if len(stops_element) > 1 and stops_element[1] else None #get the second element


    # Price
    price_element = soup.find('h5', {'data-testid': 'pricing'})
    flight['price'] = price_element.text.strip() if price_element else None

    return flight

# Example usage:
if __name__ == "__main__":
    access_ixigo()