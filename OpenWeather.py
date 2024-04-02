# THUY NGUYEN
# THUYN18@UCI
# 10087312

from WebAPI import WebAPI


class OpenWeather(WebAPI):
    '''
    Connect to API and load data to transclude message
    '''

    def __init__(self, zipcode="92697", ccode='US'):
        super().__init__()
        self.zipcode = zipcode
        self.ccode = ccode
        self.apikey = None
        self.temperature = None
        self.high_temperature = None
        self.low_temperature = None
        self.longitude = None
        self.latitude = None
        self.description = None
        self.humidity = None
        self.city = None
        self.sunset = None

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores
        the response in class data attributes.

        '''
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}"
        data = self._download_url(url)

        if data:
            self.temperature = data['main']['temp']
            self.high_temperature = data['main']['temp_max']
            self.low_temperature = data['main']['temp_min']
            self.longitude = data['coord']['lon']
            self.latitude = data['coord']['lat']
            self.description = data['weather'][0]['description']
            self.humidity = data['main']['humidity']
            self.city = data['name']
            self.sunset = data['sys']['sunset']

    def transclude(self, message: str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        '''
        if '@weather' in message:
            self.load_data()
            message = message.replace('@weather', self.description)
        if '@location' in message:
            self.load_data()
            message = message.replace('@location', self.city)
        return message
