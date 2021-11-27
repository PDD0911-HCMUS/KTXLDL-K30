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

def getAll():
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=DESKTOP-9SP3VP3\SQLEXPRESS;"
                        "Database=KTXLDL_AQI;"
                        "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    myParam = {
                "bounds": "-238.71093750000003,-62.10388252289787,239.06250000000003,78.42019327591201",
                "inc": "placeholders",
                "viewer": "webgl",
                "zoom": 2
                }
    r = requests.post(base_url + f"/mapq2/bounds", data=myParam)
    for i in range(len(r.json()['data'])):
        cityName = r.json()['data'][i]['name']
        aqi = r.json()['data'][i]['aqi']
        lat = r.json()['data'][i]['geo'][0]
        long = r.json()['data'][i]['geo'][1]
        idx = r.json()['data'][i]['idx']

        try:
            #detail
            geo = "geo:"+str(lat)+";"+str(long)
            r_detail = requests.post(base_url +  f"/feed/{geo}/?token={token}")
            string_detail = str(r_detail.json()['data']['iaqi'])
            h = r_detail.json()['data']['iaqi']['h']['v'] if 'h' in string_detail else 0
            no2 = r_detail.json()['data']['iaqi']['no2']['v'] if 'no2' in string_detail else 0
            o3 = r_detail.json()['data']['iaqi']['o3']['v'] if 'o3' in string_detail else 0
            pm25 = r_detail.json()['data']['iaqi']['pm25']['v'] if 'pm25' in string_detail else 0
            so2 = r_detail.json()['data']['iaqi']['so2']['v'] if 'so2' in string_detail else 0
            time = r_detail.json()['data']['time']['s']

            if(int(aqi) <= 50):
                rate = "Good"
            elif(int(aqi) > 50 and int(aqi) <= 100):
                rate = "Moderate"
            elif(int(aqi) > 100 and int(aqi) <= 150):
                rate = "Unhealthy for Sensitive Groups"
            elif(int(aqi) > 150 and int(aqi) <= 200):
                rate = "Unhealthy"
            elif(int(aqi) > 200 and int(aqi) <= 300):
                rate = "Very Unhealthy"
            else:
                rate = "Hazardous"

            SQLCommand = ("INSERT INTO AQI_INFORMATION(Idx, NameCity, AQIIndex, Rate, Lat, Long, CreateDate, CreateAt) VALUES (?,?,?,?,?,?,?,?)")    
            Values = [idx, cityName, aqi, rate, lat, long, date.today(), datetime.today()]
            cursor.execute(SQLCommand,Values)     
            cnxn.commit()

            SQLCommand_detail = ("INSERT INTO AQI_INFOR_DETAIL(Idx, NameCity, Lat, Long, H, No2, O3, Pm25, So2, Time, CreateDate, CreateAt) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")    
            Values_detail = [idx, cityName, lat, long, h, no2, o3, pm25, so2, time, date.today(), datetime.today()]
            cursor.execute(SQLCommand_detail,Values_detail)     
            cnxn.commit()
            
        except:
            print("Idx: {}, City: {}, AQI: {}".format(idx, cityName, aqi))
    return  
if __name__ == '__main__':
    getAll()
    