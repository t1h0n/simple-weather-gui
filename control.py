import requests
import ctypes
import locale


class WeatherRequest:
    ''' wraps requests to weather api'''

    def __init__(self, url, headers, querystring):
        self.querystring = querystring
        self.url = url
        self.headers = headers

        self.icon = None
        self.text = None
        self.errText = None
        self.errOccured = False

    def _make_request(self):
        response = requests.request(
            "GET", self.url, headers=self.headers, params=self.querystring)
        return response.json()

    def _format_response(self, response):
        place = response['name']
        description = response['weather'][0]['description']
        icon = response['weather'][0]['icon']
        temprature = response['main']['temp']
        temprature_feels = response['main']['feels_like']
        humid = response['main']['humidity']
        text = (f'Place: {place}\n'
                f'Describtion: {description}\n'
                f'Temprature(C): {temprature},\n'
                f'feels like {temprature_feels}\n'
                f'Humidity: {humid}')
        self.icon = icon
        self.text = text

    def make_request(self):
        try:
            response = self._make_request()
            if response['cod'] is 200:
                self._format_response(response)
            else:
                self.errText = response['message']
                self.errOccured = True
        except (requests.exceptions.RequestException):
            self.errText = ' failed to make a request'
            self.errOccured = True

    def getIcon(self):
        return self.icon

    def getText(self):
        return self.text

    def failedToGetResponse(self):
        return self.errOccured

    def getErrorMessage(self):
        return self.errText

    @staticmethod
    def MakeRequest(url, headers, querystring):
        weather_req = WeatherRequest(url, headers, querystring)
        weather_req.make_request()
        return weather_req


class WeahterAppModel:
    def __init__(self):
        self.system_language = WeahterAppModel.get_system_language()
        self.w = None

    def MakeRequest(self, location):
        self.w = WeatherRequest.MakeRequest(
            url="https://community-open-weather-map.p.rapidapi.com/weather",

            querystring={"q": location,
                         "lang": self.system_language,
                         "units": "metric"},

            headers={
                'x-rapidapi-key': "f6ad22cc6emsh303a4e1909cb563p128d60jsne1733d84f0f6",
                'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
            }
        )

    def getIcon(self):
        return self.w.getIcon()

    def getText(self):
        return self.w.getText()

    def failedToGetResponse(self):
        return self.w.failedToGetResponse()

    def getErrorMessage(self):
        return self.w.getErrorMessage()

    @staticmethod
    def get_system_language():
        windll = ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()
        system_language, _ = locale.windows_locale[windll.GetUserDefaultUILanguage()].split(
            '_')
        return system_language
