import csv
import requests
import json
from datetime import datetime, timedelta


def writeToCSV(keys, data):  # keys is a list of keys, data is a list of dicts
    # Writing the data to a CSV file
    with open('historicWeatherData.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(keys)
        # Write the data row
        for i in range(len(data)):
            writer.writerow(data[i].values())


def clearCSV():
    with open('historicWeatherData.csv', 'w') as file:
        file.write('')


class getWeatherData:

    def __init__(self, zipcode):  # takes in zipcode for location

        self.zipcode = zipcode
        self.currentWeatherData = {}
        self.historicWeatherMetaData = {}
        self.hourlyDataPoints = []

    def getDataCurrent(self):
        # make an api request with given zipcode
        r = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=0fcfa513412f45c197842401231007&q={self.zipcode}&aqi=no")
        # take request response and convert into a dictionary
        data = json.dumps(r.json(), sort_keys=True, indent=4)
        dataDic = json.loads(data)

        # extract only desired data points
        keys = ['name', 'region', 'temp_f', 'condition', 'wind_mph', 'wind_dir', 'precip_in', 'humidity',
                'feelslike_f', 'uv']

        extracted_data = {
            key: dataDic['location'][key] if key in dataDic['location'] else dataDic['current'][key] for key
            in keys}
        extracted_data['condition'] = extracted_data['condition']['text']
        self.currentWeatherData = extracted_data

    def getHourlyData(self, date):
        # make an api request with given zipcode
        r = requests.get(
            f"https://api.weatherapi.com/v1/history.json?key=0fcfa513412f45c197842401231007&q={self.zipcode}&dt={date}")
        # take request response and convert into a dictionary
        data = json.dumps(r.json(), sort_keys=True, indent=4)
        dataDic = json.loads(data)
        keys = ['country', 'name', 'region', 'localtime']
        self.historicWeatherMetaData = {key: dataDic['location'].get(key) for key in keys}

        hourKeys = ['precip_in', 'humidity', 'temp_f', 'cloud', 'uv', 'wind_mph', 'wind_degree', 'time', 'gust_mph']
        for hour in range(len(dataDic['forecast']['forecastday'][0]['hour'])):
            self.hourlyDataPoints.append({Key: dataDic['forecast']['forecastday'][0]['hour'][hour].get(Key) for Key in
                                          hourKeys})

        writeToCSV(hourKeys, self.hourlyDataPoints)

    def getDataHistoric(self):
        # get formatted date strings for use in api call
        today = datetime.today().date()
        for i in range(5):
            date = today - timedelta(days=i + 1)
            formatedDate = date.strftime('%Y-%m-%d')
            clearCSV()
            self.getHourlyData(formatedDate)

    def printCurrent(self):
        print(f"{self.currentWeatherData.get('name')}, {self.currentWeatherData.get('region')} is "
              f"{self.currentWeatherData.get('condition')} at {self.currentWeatherData.get('temp_f')} degrees."
              f"\nIt feels like {self.currentWeatherData.get('feelslike_f')} with {self.currentWeatherData.get('humidity')} percent humidity"
              f" and a UV index of {self.currentWeatherData.get('uv')}")

    def printHistoricMetaData(self):
        print(
            f'Here are weather, wind, and uv graphs for the past five days in {self.historicWeatherMetaData["name"]}, {self.historicWeatherMetaData["region"]}.')
