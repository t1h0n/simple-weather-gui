import tkinter as tk
import requests
import ctypes
import locale


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = 0
        self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify='center',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


class WeatherApp(tk.Frame):
    def __init__(self,  master=None):
        super().__init__(master, bg='#5caeb5')

        self.system_language = self.get_system_language()
        self.create_widgets()
        self.create_bindings()

    def create_widgets(self):
        self.serach_frame = tk.Frame(self)
        self.serach_frame.place(relx=0, rely=0.1, relwidth=0.8)

        self.county_entry = tk.Entry(self.serach_frame, font=('Times', 24))
        self.county_entry.pack(fill='both', expand=True, side='left')
        self.county_entry.focus()

        button_image = self.load_icon('weather-app')
        self.get_weather_button = tk.Button(
            self.serach_frame,
            image=button_image,
            command=lambda: self.get_weather(self.county_entry.get())
        )
        self.get_weather_button.image = button_image
        self.get_weather_button.pack(fill='both', expand=True)

        self.output_frame = tk.Frame(self, bg='white')
        self.output_frame.place(relx=0, rely=0.31, relwidth=0.8, relheight=0.6)

        self.output_label = tk.Label(
            self.output_frame,
            bg='white',
            justify='left',
            anchor='nw',
            font=('Times', 18)
        )
        self.output_label.font = button_image
        self.output_label.pack(side='left', fill='both', expand=True)

        self.icon_place = tk.Canvas(
            self.output_frame,
            width=50,
            height=50,
            bd=0,
            highlightthickness=0,
            bg='white'
        )
        self.icon_place.pack(anchor='ne')

    def create_bindings(self):
        self.master.bind('<Return>', self.button_pressed)
        self.button_hover = CreateToolTip(
            self.get_weather_button, 'press enter to get the weather')

    def get_weather(self, location):
        response = self.make_request(location)
        if WeatherApp.response_is_valid(response):
            weather, icon_name = self.format_response(response)
            self.display_weather(weather, icon_name)
        else:
            self.output_label['text'] = 'failed to get information'
            self.icon_place.delete('all')

    @staticmethod
    def response_is_valid(response):
        return True if response is not None and response['cod'] == 200 else False

    def button_pressed(self, event):
        self.get_weather(self.county_entry.get())

    def display_weather(self, weather, icon_name):
        self.output_label['text'] = weather
        img = WeatherApp.load_icon(icon_name)
        self.icon_place.delete('all')
        self.icon_place.create_image(25, 25, image=img)
        self.icon_place.image = img

    def format_response(self, response):
        place = response['name']
        description = response['weather'][0]['description']
        icon = response['weather'][0]['icon']
        temprature = response['main']['temp']
        temprature_feels = response['main']['feels_like']
        humid = response['main']['humidity']
        message = (f'Place: {place}\n'
                   f'Describtion: {description}\n'
                   f'Temprature(C): {temprature},\n'
                   f'feels like {temprature_feels}\n'
                   f'Humidity: {humid}')

        return message, icon

    def make_request(self, location):
        url = "https://community-open-weather-map.p.rapidapi.com/weather"

        querystring = {"q": location,
                       "lang": self.system_language,
                       "units": "metric"}

        headers = {
            'x-rapidapi-key': "f6ad22cc6emsh303a4e1909cb563p128d60jsne1733d84f0f6",
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        return response.json()

    @staticmethod
    def load_icon(image_name, image_ext='png', path='./images'):
        image = tk.PhotoImage(file=f'{path}/{image_name}.{image_ext}')
        return image

    def get_system_language(self):
        windll = ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()
        system_language, _ = locale.windows_locale[windll.GetUserDefaultUILanguage()].split(
            '_')
        return system_language


def main():
    root = tk.Tk()
    root.title('Weather')
    w = WeatherApp(root).pack(fill='both', expand=True)
    root.minsize(600, 400)
    root.mainloop()


if __name__ == '__main__':
    main()
