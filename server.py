from flask import Flask, request
import json
from os.path import exists

app = Flask(__name__)
FILE = 'captured.txt'

def create_file_if_not_exists():
    if exists(FILE):
        return

    with open(FILE, 'w') as file:
        file.write('unix;characteristic;data\n')


def process(data):
    unix = data['unix']
    characteristic = data['characteristic']
    data = data['data']
    
    with open(FILE, 'a') as file:
        file.write(f"{unix};{characteristic};{data}\n")

@app.route("/", methods=["POST"])
def hello_world():
    data_list = json.loads(request.data)
    if type(data_list) != list:
        return "No data"

    for data in data_list:
        process(data)

    return "Ok"
   


if __name__ == "__main__":
    create_file_if_not_exists()
    app.run(debug=True, host="0.0.0.0")