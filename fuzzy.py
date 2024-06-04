import argparse
import numpy as np
import matplotlib.pyplot as plt


class Temperature:
    def __init__(self, x):
        self.temp = x
        self.freezing = self.temp_freezing()
        self.cool = self.temp_cool()
        self.warm = self.temp_warm()
        self.hot = self.temp_hot()
        
    def temp_freezing(self):
        if 0 <= self.temp < 30:
            freezing = 1
        elif 30 < self.temp < 50:
            freezing = -0.05 * self.temp + 2.5
        elif 50 <= self.temp <= 110 :
            freezing = 0
        return freezing

    def temp_cool(self):
        if 0 <= self.temp <= 30:
            cool = 0
        elif 30 < self.temp < 50:
            cool = 0.05 * self.temp - 1.5
        elif self.temp == 50:
            cool = 1
        elif 50 < self.temp < 70:
            cool = -0.05 * self.temp + 3.5
        elif 70 <= self.temp <= 110:
            cool = 0
        return cool
    
    def temp_warm(self):
        if 0<= self.temp <= 50:
            warm = 0
        elif 50 < self.temp < 70:
            warm = 0.05 * self.temp -2.5
        elif self.temp == 70:
            warm = 1
        elif 70 < self.temp < 90:
            warm = -0.05 * self.temp + 4.5
        elif 90 <= self.temp <= 110:
            warm = 0
        return warm

    def temp_hot(self):
        if 0 <= self.temp <= 70:
            hot = 0
        elif 70 < self.temp < 90:
            hot = 0.05 * self.temp - 3.5
        elif 90 <= self.temp <= 110:
            hot = 1
        return hot
    

class Weather():
    def __init__(self, x):
        self.cast = x
        self.sunny = self.weather_sunny()
        self.cloudy = self.weather_partiallyCloudy()
        self.overcast = self.weather_overcast()

    def weather_sunny(self):
        if 0 <= self.cast <= 20:
            sunny = 1
        elif 20 < self.cast < 40:
            sunny = -0.05 * self.cast + 2
        elif self.cast >= 40 and self.cast <=110:
            sunny = 0
        return sunny

    def weather_partiallyCloudy(self):
        if 0 <= self.cast <= 20 or 80 <= self.cast <=110:
            cloudy = 0
        elif 20 < self.cast < 50:
            cloudy = 0.0333 * self.cast - 0.667
        elif self.cast == 50:
            cloudy = 1
        elif  50 < self.cast < 80:
            cloudy = -0.0333 * self.cast + 2.667
        return cloudy
        
    def weather_overcast(self):
        if 0 <= self.cast <= 60:
            overcast = 0
        elif 60 < self.cast < 80:
            overcast = 0.05 * self.cast -3
        elif 80 <= self.cast <= 110:
            overcast = 1
        return overcast

class Speed:
    def __init__(self, temp_warm, temp_cool, weather_sunny, weather_cloudy):
        self.slow_degree = min(temp_cool, weather_cloudy)
        self.fast_degree = min(temp_warm, weather_sunny)
        self.speeds = np.linspace(0, 110, 1000)
        self.slow_output = []
        self.fast_output = []
        self.orig_slow = [self.slow(x) for x in self.speeds]
        self.orig_fast = [self.fast(x) for x in self.speeds]

    def get_speed(self):
        self.slow_output = [min(self.slow(speed), self.slow_degree) for speed in self.speeds]
        self.fast_output = [min(self.fast(speed), self.fast_degree) for speed in self.speeds]
        
        numerator = np.sum(self.speeds * self.slow_output) + np.sum(self.speeds * self.fast_output)
        denominator = np.sum(self.slow_output) + np.sum(self.fast_output)
        
        if denominator == 0:
            return 0
        else:
            return numerator / denominator

    def slow(self, speed):
        if speed < 25:
            return 1
        elif 25 <= speed < 75:
            return -0.02 * speed + 1.5
        elif speed >= 75:
            return 0
        
    def fast(self, speed):
        if speed < 25:
            return 0
        elif 25 <= speed < 75:
            return 0.02 * speed - 0.5
        elif speed >= 75:
            return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Computes the speed using temparatures")
    parser.add_argument("--temp", type=float, required=True, help="Temperature to calculate")
    parser.add_argument("--cloud", type=float, required=True, help="Temperature to calculate")

    args = parser.parse_args()

    temp = Temperature(round(args.temp, 2))
    cloud = Weather(round(args.cloud, 2))

    speed = Speed(temp.warm, temp.cool, cloud.sunny, cloud.cloudy)
    
    print(f"Temperature = {temp.temp}: \n{temp.freezing*100:.2f}% Freezing.\n{temp.cool*100:.2f}% Cool.\n{temp.warm*100:.2f}% Warm.\n{temp.hot*100:.2f}% Hot.\n")
    print(f"Weather = {cloud.cast}: \n{cloud.sunny*100:.2f}% Sunny.\n{cloud.cloudy*100:.2f}% Partly Cloudy.\n{cloud.overcast*100:.2f}% Overcast.\n")
    print(f"Speed: {speed.get_speed()} mph")

    plt.plot(speed.speeds, speed.slow_output, label="slow output", color='red')
    plt.plot(speed.speeds, speed.fast_output, label="fast output", color='blue')
    plt.plot(speed.speeds, speed.orig_slow, linestyle='dashed', color='red')
    plt.plot(speed.speeds, speed.orig_fast, linestyle='dashed', color='blue')
    plt.fill_between(speed.speeds, speed.slow_output, alpha=1, color='gray')
    plt.fill_between(speed.speeds, speed.fast_output, alpha=1, color='gray')
    plt.xlabel('Speed')
    plt.ylabel('Values')
    plt.axis([0,110,0,1.2])
    plt.legend()
    plt.show()
