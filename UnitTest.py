import unittest
from OpenWeather import OpenWeather
from LastFM import LastFM


class TestOpenWeather(unittest.TestCase):
    '''
    Testing Open Weather functions
    '''
    def test_load_data(self):
        '''
        Testing load_data function for Open_Weather module
        '''
        api_key = "0b72015c070f9952c0a1c40847ec8557"
        open_weather = OpenWeather()
        open_weather.set_apikey(api_key)
        open_weather.load_data()

        assert open_weather.description == f'{open_weather.description}'
        assert open_weather.city == "Irvine"

    def test_transclude_weather(self):
        '''
        Testing transclude_weather function for Open_Weather module
        '''
        api_key = "0b72015c070f9952c0a1c40847ec8557"
        message = "It's @weather today."
        open_weather = OpenWeather()
        open_weather.set_apikey(api_key)


        transcluded_message = open_weather.transclude(message)
        desc = open_weather.description
        assert transcluded_message == f"It's {desc} today."

class TestLastFM(unittest.TestCase):
    '''
    Testing Open Weather functions
    '''
    def test_LastFM(self):
        '''
        Testing LastFM module
        '''

        api_key = '024c7c1f2a5d26e35a207c6d17a44f27'
        lastfm = LastFM()
        lastfm.set_apikey(api_key)
        lastfm.load_data()
        response = lastfm.transclude('top artist: @lastfm')

        self.assertEqual(response, 'top artist: The Weeknd', 'Failed to parse top artist correctly!')

if __name__ == '__main__':
    unittest.main()
