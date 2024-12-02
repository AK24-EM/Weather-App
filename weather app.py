import tkinter as tk
from datetime import datetime
import requests

class WeatherApp:
    def __init__(self ,  root , api_key):
        self.root = root
        self.api_key = api_key
        self.root.title("weather app")
        self.create_widgets()

    def create_widgets(self):
        self.clear()
        tk.Label(self.root , text="enter your name").pack(pady=5)
        self.location_entry = tk.Entry(self.root)
        self.location_entry.pack(pady=5)

        button = tk.Button(self.root , text= "get weather" , command = self.weather)
        button.pack(pady=5)

        self.result_label =tk.Label(self.root , text=" ")
        self.result_label.pack(pady=5)

        button1 = tk.Button(self.root , text= "try again" , command = self.create_widgets)
        button1.pack(pady=5)

    def temperature(self , kelvin):
        celsius = kelvin - 273.15
        fahrenheit = 9/5* celsius + 32
        return celsius  ,  fahrenheit

    def weather(self):
        print("Button clicked")
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        city = self.location_entry.get()
        print(f"City entered: {city}")
        if not city:
            self.result_label.config(text="Please enter a city name.")
            return

        url = f"{BASE_URL}q={city}&appid={self.api_key}"
        try:
            response = requests.get(url).json()
            if response.get("cod") != 200:
                self.result_label.config(text=f" city no found, pls try again later")
                return

            temp_kelvin = response['main']['temp']
            temp_celsius  , temp_fahrenheit= self.temperature(temp_kelvin)
            wind_speed = response['wind']['speed']
            humidity = response['main']['humidity']
            description = response['weather'][0]['description']
            sunrise_time = datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
            sunset_time = datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
            self.result_label.config(
                text=(
                    f"Weather: {description.capitalize()}\n"
                    f"Temperature: {temp_celsius:.2f}°C / {temp_fahrenheit:.2f}°F\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind Speed: {wind_speed} m/s\n"
                    f"Sunrise: {sunrise_time.strftime('%H:%M:%S')} UTC\n"
                    f"Sunset: {sunset_time.strftime('%H:%M:%S')} UTC\n"
                )
            )
        except Exception as e :
            self.result_label.config(text="Error fetching data. Check your connection.")
            print(e)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    api_key = "b1690b6d937fd41b3fbaadaf85953edb"
    app = WeatherApp(root, api_key )
    root.mainloop()


