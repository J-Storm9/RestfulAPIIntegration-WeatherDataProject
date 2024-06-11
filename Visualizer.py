import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb


class Visualizer:
    def __init__(self):
        self.df = pd.read_csv(r"historicWeatherData.csv")

    def tempGraph(self):
        # TODO change x axis name
        minTemp = self.df['temp_f'].min()
        plt.plot(self.df['time'], self.df['humidity'] / 10 + minTemp, linestyle='-', color='red', label="Humidity")
        plt.fill_between(self.df['time'], self.df['humidity'] / 10 + minTemp, minTemp - 5, alpha=0.1, color='red')
        plt.plot(self.df['time'], self.df['temp_f'], linestyle='-', color='orange', label="Temperature")
        plt.plot(self.df['time'], (self.df['precip_in'] * 5) + minTemp - 5, linestyle='-', color='blue',
                 label="Precipitation")
        plt.legend(loc='best')
        plt.title("Temperature, Humidity, and Rain")
        plt.xticks(np.arange(1, 120, 14), rotation=45)
        plt.margins(x=0, y=0.05, tight=True)
        plt.subplots_adjust(bottom=0.25)
        plt.show()

    def uvGraph(self):
        df = self.df[['uv', 'temp_f']]
        regPlot = sb.regplot(x='uv', y='temp_f', data=df, line_kws={'color': 'red'})
        regPlot.set_title('Correlation Between UV and Temperature')

        plt.grid(True)
        plt.show()

    def windGraph(self):
        dirRad = np.radians(np.array(self.df['wind_degree']))
        speed = np.array(self.df['wind_mph'])
        gust = np.array(self.df['gust_mph'])

        fig, axes = plt.subplots(ncols=2, figsize=(10, 4), subplot_kw={"projection": "polar"})
        cmap = 'inferno_r'
        for ax in axes:
            if ax == axes[1]:
                vals, _, _, img = ax.hist2d(dirRad, speed,
                                            bins=(
                                                np.linspace(0, 2 * np.pi, 37), np.linspace(min(speed), max(speed), 16)),
                                            weights=gust, cmap=cmap, vmin=0, vmax=max(gust) * 1.1, cmin=0.00001)
            else:
                img = ax.scatter(dirRad, speed, c=gust, cmap=cmap, vmin=0, vmax=max(gust) * 1.1)
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            plt.colorbar(img, ax=ax, pad=0.12, label='Wind Gust MPH')
        plt.title("Wind direction, speed, and gust")
        plt.show()
