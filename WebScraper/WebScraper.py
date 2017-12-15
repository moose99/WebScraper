import requests
import bs4
import pandas as pd

#
# Scrapes 7 day weather forecast data from this URL
#
PAGE_URL = 'http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168'

class WebScraper:
    # Download the web page containing the forecast.
    # Create a BeautifulSoup class to parse the page.
    # Find the div with id seven-day-forecast, and assign to seven_day
    def __init__(self, **kwargs):
        page = requests.get(PAGE_URL)
        self.soup = bs4.BeautifulSoup(page.content, 'html.parser')
        return super().__init__(**kwargs)

    # Inside seven_day, find each individual forecast item.
    # note: since class is a reserved word, we will use class_
    def GetSevenDayForecast(self):
        self.seven_day = self.soup.find(id="seven-day-forecast")
        self.forecast_items = self.seven_day.find_all(class_="tombstone-container")

    # Extract and print the first forecast item.
    def PrintTonightsForecast(self):
        tonight = self.forecast_items[0]
        print('TONIGHTS FORECAST HTML')
        print(tonight.prettify())

    # Select all items with the class period-name inside an item with the class tombstone-container in seven_day.
    # Use a list comprehension to call the get_text method on each BeautifulSoup object.
    def ExtractSevenDayData(self):
        period_tags = self.seven_day.select(".tombstone-container .period-name")
        periods = [pt.get_text() for pt in period_tags]

        # Now get 3 other fields
        short_descs = [sd.get_text() for sd in self.seven_day.select(".tombstone-container .short-desc")]
        temps = [t.get_text() for t in self.seven_day.select(".tombstone-container .temp")]
        descs = [d["title"] for d in self.seven_day.select(".tombstone-container img")]

        # Combine the data into a Pandas DataFrame and analyze it
        # Make a column out of each list
        self.weather = pd.DataFrame({
                "period": periods, 
                "short_desc": short_descs, 
                "temp": temps, 
                "desc":descs
            })
        print('\nWEATHER DATA TABLE')
        print(self.weather)

    # use a regular expression and the Series.str.extract method to pull out the numeric temperature values:
    def GetTemps(self):
        temp_nums = self.weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
        self.weather["temp_num"] = temp_nums.astype('int')
        print('\nWEATHER TEMPS and MEAN')
        print(temp_nums)
        print(self.weather["temp_num"].mean())

    #  only select the rows that happen at night:
    def GetNights(self):
        is_night = self.weather["temp"].str.contains("Low")
        self.weather["is_night"] = is_night
        print('\nNIGHT DATA')
        print(is_night)
        print(self.weather[is_night])

#
# MAIN
#
scraper = WebScraper()
scraper.GetSevenDayForecast()
scraper.PrintTonightsForecast()
scraper.ExtractSevenDayData()
scraper.GetTemps()
scraper.GetNights()


