import requests
import xmltodict
import time
from tabulate import tabulate

class Trains:
    def __init__(self, credentials):
        self.credentials = credentials

    def getDepartingTrains(self, station_from):
        self.constructURL(station_from)
        resp = requests.get(self.request_url, auth=\
                (self.credentials.getUser(),\
                self.credentials.getPassword()))
        avt = xmltodict.parse(resp.content)
        trains = []
        for train in avt['ActueleVertrekTijden']['VertrekkendeTrein']:
            number = train['RitNummer']
            destination = train['EindBestemming']
            train_type = train['TreinSoort']
            platform = train['VertrekSpoor']['#text']
            departure_time = train['VertrekTijd']         
            departure_time = time.strptime(departure_time, "%Y-%m-%dT%H:%M:%S+0200")
            departure_time = time.strftime("%H:%M", departure_time)
            trains.append([destination, platform, departure_time, train_type])
        return tabulate(trains, headers=['Destination', 'Platform', 'Time', 'Type'])


    def constructURL(self, station_from):
        self.request_url =\
                'https://webservices.ns.nl/ns-api-avt?station={}'\
                .format(station_from)

        
