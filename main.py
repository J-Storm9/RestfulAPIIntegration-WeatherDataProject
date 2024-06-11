from getWeatherData import getWeatherData
from UserInteraction import *
from Visualizer import *

if __name__ == '__main__':

    while True:
        UI = UserInteraction()
        UI.promptZipcode()

        while not UI.validPostalCode():
            UI.promptZipcode()

        if UI.promptCrrentOrHistoric():
            data = getWeatherData(UI.zipcode)
            data.getDataCurrent()
            data.printCurrent()
        else:
            data = getWeatherData(UI.zipcode)
            data.getDataHistoric()
            data.printHistoricMetaData()

            graphs = Visualizer()
            graphs.uvGraph()
            graphs.windGraph()
            graphs.tempGraph()


        UI.inputAgain()
