import argparse
from settings import Credentials
from trains import Trains
from flask import Flask
from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
)

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

@app.route('/help')
def help():
    msg = "Station names consisting of 2 parts need a + sign.\n"
    msg += "For example: Den+Bosch\n"
    return msg

@app.route('/')
def home():
    return "Try adding <station> to get current departure times.\n"
   
@app.route('/<string:station>')
@limiter.limit("50 per day")
def departingTrains(station):
    print(request.args.to_dict())
    train_info = Trains(Credentials())
    return train_info.getDepartingTrains(station) + '\n'

if __name__=="__main__":
    app.run(host='127.0.0.1')
