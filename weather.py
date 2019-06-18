import urllib.request
import json
import os.path
import time

class weather_now:
    def __init__(self):
        self.__url = 'https://free-api.heweather.net/s6/weather/now?location=auto_ip&key=63f9263816ac48d7a51208ca512d8d25'
        self.__weather_data = urllib.request.urlopen(self.__url).read()
        self.__weather_dict = json.loads(self.__weather_data.decode('UTF-8')).get("HeWeather6")[0]
        self.__time = time.localtime()

    
    def status(self):
        if self.__weather_dict.get('status') == 'ok':
            return True
        else: return False 
    
    def location(self):
        if self.status():
            return self.__weather_dict.get('basic').get('location')
        else: return '错误'

    def condition(self):
        if self.status():
            return self.__weather_dict.get('now').get('cond_txt')
        else:
            return '错误'

    def cond_icon(self):
        if self.status():
            self.__icon = self.__weather_dict.get('now').get('cond_code')
            if self.__time.tm_hour >= 18 or self.__time.tm_hour <= 6:
                if self.__icon in ['100', '103', '104', '300', '301', '406', '407']:
                    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'cond-icon', self.__icon + 'n.png'))
                else:
                    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'cond-icon', self.__icon + '.png'))
            else:
                return os.path.abspath(os.path.join(os.path.dirname(__file__), 'cond-icon', self.__icon + '.png'))
        else:
            return os.path.abspath(os.path.join(os.path.dirname(__file__), 'cond-icon', '999.png'))

    def temperature(self):
        if self.status():
            return self.__weather_dict.get('now').get('tmp') + '℃'
        else:
            return 'N/A'


class weather_forecast:
    def __init__(self):
        self.__url = 'https://free-api.heweather.net/s6/weather/forecast?location=auto_ip&key=63f9263816ac48d7a51208ca512d8d25'
        self.__weather_data = urllib.request.urlopen(self.__url).read()
        self.__weather_dict = json.loads(self.__weather_data.decode('UTF-8')).get("HeWeather6")[0]
        self.__time = time.localtime()

    def status(self):
        if self.__weather_dict.get('status') == 'ok':
            return True
        else:
            return False

    def daily_forecast(self, day):
        if self.status():
            return self.__weather_dict.get('daily_forecast')[day]

    def condition(self, day):
        if self.status():
            cond_d = self.daily_forecast(day).get('cond_txt_d')
            if '到' in cond_d:
                cond_d = cond_d.split('到')[1]
            cond_n = self.daily_forecast(day).get('cond_txt_n')
            if '到' in cond_n:
                cond_n = cond_n.split('到')[1]
            if cond_d == cond_n:
                return cond_d
            else:
                return '{}转{}'.format(cond_d, cond_n)
        else:
            return '错误'

    def cond_icon(self, day):
        if self.status():
            self.__icon = self.daily_forecast(day).get('cond_code_d')
            return os.path.abspath(os.path.join(os.path.dirname(__file__), 'cond-icon', self.__icon + '.png'))
        else:
            return os.path.abspath(os.path.join(os.path.dirname(__file__), 'cond-icon', '999.png'))

    def temperature(self, day):
        if self.status():
            return '{}/{}℃'.format(self.daily_forecast(day).get('tmp_max'), self.daily_forecast(day).get('tmp_min'))
        else:
            return 'N/A'
