import requests
import xmltodict
import time
from settings import Credentials
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
    
    def getDisruptions(self, message=False):
        self.disrupt_url =\
                'https://webservices.ns.nl/ns-api-storingen?actual=true'
        resp = requests.get(self.disrupt_url, auth=\
                (self.credentials.getUser(),\
                self.credentials.getPassword()))
        disrupt = xmltodict.parse(resp.content)
        #print(disrupt['Storingen']['Gepland']['Storing'].items())
        disruptions = []
        message_string = ""
        if len(disrupt['Storingen']['Ongepland']['Storing']) != 0:
            for item in disrupt['Storingen']['Ongepland']['Storing']:
                traject = item['Traject']
                reason = item['Reden']
                if message:
                    message = item['Bericht']
                    disruptions.append([traject, reason, message])
                else:
                    disruptions.append([traject, reason])
            if message:
                message_string += tabulate(disruptions,\
                        headers=['Route', 'Reason', 'Message'])
            else: 
                message_string += tabulate(disruptions, headers=['Route', 'Reason'])
        works = []
        message_string += '\n'
        if len(disrupt['Storingen']['Gepland']['Storing']) != 0:
            for item in disrupt['Storingen']['Gepland']['Storing']:
                traject = item['Traject']
                periode = item['Periode']
                if message:
                    message = item['Bericht']
                    works.append([traject, periode, message])
                else:
                    works.append([traject, periode])
            if message:
                message_string += tabulate(works,\
                        headers=['Route', 'From/Till', 'Message'])
            else:
                message_string += tabulate(works, headers=['Route', 'From/Till'])
        return message_string

    def constructURL(self, station_from):
        self.request_url =\
                'https://webservices.ns.nl/ns-api-avt?station={}'\
                .format(station_from)

if __name__=="__main__":
    train_info = Trains(Credentials())
    train_info.getDisruptions()
