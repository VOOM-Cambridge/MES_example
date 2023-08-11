import requests
from http.client import HTTPSConnection
from base64 import b64encode



# Basic set up code 
def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

BASE_URL = "http://localhost:9000/"
username = "admin"
password = "admin"

payload = {}
headers = {
  'Authorization': basic_auth(username, password)
  }


def getDataOrders():
    url = BASE_URL + "api/input/demand/"
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print('Get data failed:' + response.status_code)
        return None

def itemsFunc(process, data):
    url = BASE_URL + "/api/input/item/"
    payload =     {
        "name": "",
        "owner": None,
        "description": "",
        "category": "",
        "subcategory": "",
        "cost": None,
        "volume": None,
        "weight": None,
        "uom": "",
        "type": None,
        "source": ""
        }
    match process:
        case "GET":
            pros = "GET"
            payload = None
        case "ADD":
            pros = "POST"
            payload["name"] = data["name"]
            payload["cost"] = data["cost"]
            payload["description"] = data["description"]
        case "REMOVE":
            pros = "DELETE"
            url = url + data["name"].replace(" ", "%20")
        case "EDIT":
            pros = "PUT"
            payload["name"] = data["name"]
            payload["cost"] = data["cost"]
            payload["description"] = data["description"]
        case default:
            pros = "GET"
            payload = None

    response = requests.request(pros, url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print('Get data failed:' + response.status_code)
        return None

def runPlan():
    url = BASE_URL + "/execute/api/runplan/"
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print('Get data failed:' + response.status_code)
        return None


# main python function
if __name__ == "__main__":
    # data = getDataOrders()
    # print(data)
    # process = "GET"
    # inData = {}
    # dataNew = itemsFunc(process, inData)
    out = runPlan()
    print(out)

