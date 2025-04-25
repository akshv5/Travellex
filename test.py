import datetime
import pandas as pd

def load_station_codes():
    try:
        # Load station codes from all_stations.csv
        station_df = pd.read_csv('all_stations.csv')
        # Create a dictionary of station name to station code
        return dict(zip(station_df['Station Name'].str.lower(), station_df['Station Code']))
    except FileNotFoundError:
        return {}

def load_airport_codes():
    try:
        # Load airport codes from airports_data.csv
        airports_df = pd.read_csv('airports_data.csv')
        # Create a dictionary of city to IATA code
        airport_codes = dict(zip(airports_df['City'].str.lower(), airports_df['IATA Code']))
        
        # Add major Indian cities that might be missing
        major_cities = {
            'delhi': 'DEL',
            'mumbai': 'BOM',
            'bangalore': 'BLR',
            'chennai': 'MAA',
            'kolkata': 'CCU',
            'hyderabad': 'HYD',
            'ahmedabad': 'AMD',
            'pune': 'PNQ',
            'jaipur': 'JAI',
            'goa': 'GOI'
        }
        airport_codes.update(major_cities)
        return airport_codes
    except FileNotFoundError:
        return {}

def format_date(date_str):
    """Convert YYYY-MM-DD to DDMMYYYY format"""
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%d%m%Y')

def generate_train_link(from_city, to_city, travel_date, adults=1, children=0, infants=0, seniors=0, students=0):
    station_codes = load_station_codes()
    
    # Convert cities to lowercase for matching
    from_city_lower = from_city.lower()
    to_city_lower = to_city.lower()
    
    # Get station codes
    from_station = station_codes.get(from_city_lower, '')
    to_station = station_codes.get(to_city_lower, '')
    
    if not from_station or not to_station:
        return "Error: City not found in station database"
    
    # Format date
    formatted_date = format_date(travel_date)
    
    # Construct the train booking URL
    train_url = f"https://www.ixigo.com/search/result/train/{from_station}/{to_station}/{formatted_date}//{adults}/{children}/{seniors}/{students}/ALL"
    
    return train_url

def generate_flight_link(from_city, to_city, from_date, return_date=None, adults=1, children=0, infants=0, travel_class='e'):
    airport_codes = load_airport_codes()
    
    # Convert cities to lowercase for matching
    from_city_lower = from_city.lower()
    to_city_lower = to_city.lower()
    
    # Get airport codes
    from_airport = airport_codes.get(from_city_lower, '')
    to_airport = airport_codes.get(to_city_lower, '')
    
    if not from_airport or not to_airport:
        return "Error: City not found in airport database"
    
    # Format dates
    formatted_from_date = format_date(from_date)
    formatted_return_date = format_date(return_date) if return_date else ''
    
    # Construct the flight booking URL
    flight_url = f"https://www.ixigo.com/search/result/flight?from={from_airport}&to={to_airport}&date={formatted_from_date}"
    
    if return_date:
        flight_url += f"&returnDate={formatted_return_date}"
    
    flight_url += f"&adults={adults}&children={children}&infants={infants}&class={travel_class}&source=Search+Form"
    
    return flight_url

# Example usage
if __name__ == "__main__":
    # Example inputs
    from_city = "Delhi"
    to_city = "Mumbai"
    from_date = "2025-04-30"
    to_date = "2025-05-04"
    
    # Get passenger counts
    adults = 2
    children = 3
    infants = 0
    seniors = 0
    students = 0
    
    # Generate train link
    train_link = generate_train_link(
        from_city=from_city,
        to_city=to_city,
        travel_date=from_date,
        adults=adults,
        children=children,
        infants=infants,
        seniors=seniors,
        students=students
    )
    
    # Generate flight link
    flight_link = generate_flight_link(
        from_city=from_city,
        to_city=to_city,
        from_date=from_date,
        return_date=to_date,
        adults=adults,
        children=children,
        infants=infants,
        travel_class='e'  # e for economy
    )
    
    print("Train Booking Link:")
    print(train_link)
    print("\nFlight Booking Link:")
    print(flight_link)