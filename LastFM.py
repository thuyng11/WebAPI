# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

from WebAPI import WebAPI


class LastFM(WebAPI):
    '''
    Connect to API and load data to transclude message
    '''
    def __init__(self, page=1, limit=1) -> None:
        super().__init__()
        self.page = page
        self.limit = limit
        self.top_artists = None

    def load_data(self):
        '''
        Calls the web api using the required values and stores the
        response in class data attributes.
        '''
        try:
            url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={self.apikey}&limit={self.limit}&format=json"

            data = self._download_url(url)
            if data:
                self.top_artists = data['artists']['artist']
        except AttributeError as e:
            print(f'An error occured: {e}')

    def transclude(self, message: str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        '''
        try:
            keyword = '@lastfm'

            if keyword in message:
                self.load_data()
                top_artist_name = self.top_artists[0]['name'] if self.top_artists else "No top artist found"
                message = message.replace(keyword, top_artist_name)

            return message
        except AttributeError as e:
            print(f'An error occured: {e}')
