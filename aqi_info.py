import requests
import pyodbc 
from datetime import date, datetime


# read secret token from file containing the token as a single string
# you need to create this file if you want to reproduce this analysis

base_url = "https://api.waqi.info"
token = 'd1d0fc9186641b448c83b71f225d5c53ca28c629'


class AQI:
    def __init__(self, cityName, aqi, pm25):
        self.cityName = cityName
        self.aqi = aqi
        self.pm25 = pm25


class AQI_DETAIL:
    def __init__(self, cityName, aqi, pm25, lat, long, co, h, no2, o3, p, pm10, so2, t, w, time):
        self.cityName = cityName
        self.aqi = aqi
        self.pm25 = pm25
        self.lat = lat
        self.long = long
        self.co = co
        self.h = h
        self.no2 = no2
        self.o3 = o3
        self.p = p
        self.pm10 = pm10
        self.so2 = so2
        self.t = t
        self.w = w
        self.time = time


def getAQI(city):
    r = requests.get(base_url + f"/feed/{city}/?token={token}")
    cityName = r.json()['data']['city']['name']
    aqi = r.json()['data']['aqi']
    pm25 = r.json()['data']['iaqi']['pm25']['v']
    return cityName, aqi, pm25


def getDetailAQI(city):
    r = requests.get(base_url + f"/feed/{city}/?token={token}")
    # common infromation
    cityName = r.json()['data']['city']['name']
    aqi = r.json()['data']['aqi']
    pm25 = r.json()['data']['iaqi']['pm25']['v']
    # detail information
    lat = r.json()['data']['city']['geo'][0]
    long = r.json()['data']['city']['geo'][1]
    co = r.json()['data']['iaqi']['co']['v']
    h = r.json()['data']['iaqi']['h']['v']
    no2 = r.json()['data']['iaqi']['no2']['v']
    o3 = r.json()['data']['iaqi']['o3']['v']
    p = r.json()['data']['iaqi']['p']['v']
    pm10 = r.json()['data']['iaqi']['pm10']['v']
    so2 = r.json()['data']['iaqi']['so2']['v']
    t = r.json()['data']['iaqi']['t']['v']
    w = r.json()['data']['iaqi']['w']['v']
    time = r.json()['data']['time']['s']
    return cityName, aqi, pm25, lat, long, co, h, no2, o3, p, pm10, so2, t, w, time


if __name__ == '__main__':
    city = 'Paris'

    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=DESKTOP-9SP3VP3\SQLEXPRESS;"
                        "Database=KTXLDL_AQI;"
                        "Trusted_Connection=yes;")

    cursor = cnxn.cursor()

    cityName, aqi, pm25 = getAQI(city)
    aqiCls = AQI(cityName, aqi, pm25)
    SQLCommand = ("INSERT INTO AQI_INFORMATION(NameCity, AQIIndex, Pm25, CreateDate, CreateAt) VALUES (?,?,?,?,?)")    
    Values = [aqiCls.cityName, aqiCls.aqi, aqiCls.pm25, date.today(), datetime.today()]
    cursor.execute(SQLCommand,Values)     
    cnxn.commit()


    cityName, aqi, pm25, lat, long, co, h, no2, o3, p, pm10, so2, t, w, time = getDetailAQI(city)


    