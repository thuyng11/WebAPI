# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

from abc import ABC, abstractmethod
import urllib.request
import urllib.error
import json

class URLDownloadError(Exception):
    """
    Exception raised for errors in downloading content from a URL.
    """
    def __init__(self, message):
        super().__init__(message)

class DataFormatError(Exception):
    """
    Exception raised for errors in the format of downloaded data.
    """
    def __init__(self, message):
        super().__init__(message)

class HTTPError(Exception):
    '''
    Exception raised when server could not find requested information
    '''
    def __init__(self, message):
        super().__init__(message)

class BadRequestError(Exception):
    '''
    Exception raised when lost connection
    '''
    def __init__(self, message):
        super().__init__(message)

class WebAPI(ABC):
    """
    A base class for getting data from web APIs using a given API key. It defines methods for
    downloading content from URLs and setting an API key.
    """


    def __init__(self) -> None:
        self.apikey = None


    def _download_url(self, url: str) -> dict:
        ''''
        downloads  the content of a URL and returns it as a dictionary object
        '''
        response = None
        r_obj = None
        try:
            with urllib.request.urlopen(url) as response:
                json_results = response.read()
                r_obj = json.loads(json_results)
                return r_obj
        except urllib.error.HTTPError as e:
            raise HTTPError(f"{e.code} not found") from e
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                raise URLDownloadError(f"The server couldn't fulfill the request. Error code: {e.reason}") from e
            raise URLDownloadError(f'Failed to connect. Error code: {e}') from e
        except ConnectionError as e:
            raise BadRequestError(f'{e} Service Unavailable') from e
        except json.JSONDecodeError as e:
            raise DataFormatError(f'Data formatting is incorrect. Error: {e}') from e


    def set_apikey(self, apikey:str) -> None:
        '''
        set api key to access web api
        '''
        self.apikey = apikey


    @abstractmethod
    def load_data(self):
        """
        Abstract method for loading data.
        """


    @abstractmethod
    def transclude(self, message:str) -> str:
        """
        Abstract method for transcluding a message.
        """
