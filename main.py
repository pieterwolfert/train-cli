import argparse
from settings import Credentials
from trains import Trains
from flask import Flask

app = Flask(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("station_from",\
            help="from which station you want to go")
    parser.add_argument("--station_to",\
            help="to which station you want to go")
    args = parser.parse_args()
    if args.station_to:
        print("Retrieving travel information...")
    else:
        train_info = Trains(Credentials())
        print("Departing trains {}".\
                format(args.station_from.title()))
        train_info.getDepartingTrains(args.station_from)
   
@app.route('/<station>')
def departingTrains(station):
    train_info = Trains(Credentials())
    return train_info.getDepartingTrains(station)

if __name__=="__main__":
    app.run(host='127.0.0.1')
