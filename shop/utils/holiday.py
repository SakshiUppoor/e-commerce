import json
import requests


class v1:
    def __init__(self):
        self.key = 'e4bd0642-0545-4c6e-a157-e1627b17cc53'

    def holidays(self, parameters):
        url = 'https://holidayapi.com/v1/holidays?'

        if not parameters.get('key'):
            parameters['key'] = self.key
        else:
            assert self.key == parameters['key'], 'keys supplied as an argument & in `parameters` differ. \n Provide at only one place'

        response = requests.get(url, params=parameters)
        data = response.json()

        if not response.ok:
            if not data.get('error'):
                data['error'] = 'Unknown error.'

        return data


def get_holidays(country):
    obj1 = v1()
    parameters = {
        # Required
        'country': country,
        'year':    2019,
        # Optional
        # 'month':    7,
        # 'day':      4,
        # 'previous': True,
        # 'upcoming': True,
        # 'public':   True,
        # 'pretty':   True,
    }

    res = obj1.holidays(parameters)
    return res
