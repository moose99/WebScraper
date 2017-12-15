import requests
import bs4

#
# MAIN
#

# Download the web page containing the forecast.
# Create a BeautifulSoup class to parse the page.
# Find the div with id seven-day-forecast, and assign to seven_day
# Inside seven_day, find each individual forecast item.
# Extract and print the first forecast item.

page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = bs4.BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
print(tonight.prettify())
