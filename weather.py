import tkinter as tk
import requests
import ctypes
import locale


class WeatherApp(tk.Frame):
    def __init__(self,  master=None):
        super().__init__(master, bg='#5caeb5')
        self.pack(fill='both', expand=True)
        self.master.title('Weather')
        self.system_language = self.get_system_language()
        self.create_widgets()

    def create_widgets(self):
        self.serach_frame = tk.Frame(self)
        self.serach_frame.place(relx=0, rely=0.1, relwidth=0.8)

        self.county_entry = tk.Entry(self.serach_frame, font=('Times', 24))
        self.county_entry.pack(fill='both', expand=1, side='left')

        button_image = self.load_icon('weather-app')
        self.get_weather_button = tk.Button(
            self.serach_frame,
            image=button_image,
            command=lambda: self.get_weather(self.county_entry.get())
        )
        self.get_weather_button.image = button_image
        self.get_weather_button.pack()

        self.output_frame = tk.Frame(self, bg='green')
        self.output_frame.place(relx=0, rely=0.32, relwidth=0.8, relheight=0.6)

        self.output_label = tk.Label(
            self.output_frame,
            bg='white',
            justify='left',
            anchor='nw',
            font=('Times', 22)
        )
        self.output_label.font = button_image
        self.output_label.place(relwidth=1, relheight=1)

        self.icon_place = tk.Canvas(
            self.output_frame,
            width=50,
            height=50,
            bd=0,
            highlightthickness=0,
            bg='white'
        )

        self.icon_place.pack(anchor='ne')

    def get_weather(self, location):
        response = self.make_request(location)
        print(response)
        if WeatherApp.response_is_valid(response):
            weather, icon_name = WeatherApp.format_response(response)
            self.display_weather(weather, icon_name)
        else:
            self.output_label['text'] = "failed to get information"
            self.icon_place.delete('all')

    @staticmethod
    def response_is_valid(response):
        return True if response is not None and response['cod'] == 200 else False

    def display_weather(self, weather, icon_name):
        self.output_label['text'] = weather
        img = WeatherApp.load_icon(icon_name)
        self.icon_place.delete('all')
        self.icon_place.create_image(25, 25, image=img)
        self.icon_place.image = img

    @staticmethod
    def format_response(response):
        place = response['name']
        description = response['weather'][0]['description']
        icon = response['weather'][0]['icon']
        temprature = response['main']['temp']
        temprature_feels = response['main']['feels_like']
        humid = response['main']['humidity']
        return f'Place: {place}\nDescription: {description}\nTemprature(C): {temprature}, feels like {temprature_feels}\nHumidity: {humid}', icon

    def make_request(self, location):
        url = "https://community-open-weather-map.p.rapidapi.com/weather"

        querystring = {"q": location,
                       "lang": self.system_language,
                       "units": "metric"}

        headers = {
            'x-rapidapi-key': "f6ad22cc6emsh303a4e1909cb563p128d60jsne1733d84f0f6",  # GET YOUR OWN KEY!
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        return response.json()

    @staticmethod
    def load_icon(image_name, image_ext='png', path='images'):
        image = tk.PhotoImage(file=f'./{path}/{image_name}.{image_ext}')
        return image

    def get_system_language(self):
        windll = ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()
        system_language, _ = locale.windows_locale[windll.GetUserDefaultUILanguage()].split(
            '_')
        return system_language


def main():
    root = tk.Tk()
    w = WeatherApp(root)
    root.geometry("600x600")
    root.mainloop()


if __name__ == '__main__':
    main()
