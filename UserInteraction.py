# this class is for all user interaction for prompting user and input validation
import json

import requests


class UserInteraction:
    def __init__(self):
        self.zipcode = ''

    def promptZipcode(self):
        self.zipcode = input('\nPlease enter a US zip code: ')

    def validPostalCode(self):  # verify if code is a valid US zip code
        # make an api request with given zipcode
        r = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=0fcfa513412f45c197842401231007&q={self.zipcode}&aqi=no")
        # take request response and convert into a dictionary
        data = json.dumps(r.json(), sort_keys=True, indent=4)
        dataDic = json.loads(data)

        try:
            if dataDic['error']['code'] == 1006:
                print(dataDic['error']['message'])
                return False
        except KeyError as e:
            return True

    def promptCrrentOrHistoric(self):  # returns True for current and False for Historic
        response = input('\n Do you want data on current or historic weather?\n Please respond with \''
                         'current\' or \'historic\'. \nIf an invalid response is given, current will be selected.\n')
        if response == 'historic':
            return False
        else:
            return True

    def inputAgain(self):
        response = input('Would you like to get weather data on another location?(yes,no,y,n)')
        if response.upper() == 'YES' or response.upper() == 'Y':
            return True
        elif response.upper() == 'NO' or response.upper() == 'N':
            print('goodbye.')
            exit()
        else:
            print('I\'m sorry, that is an invalid response, closing program...')
            exit()

