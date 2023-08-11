import requests
from http.client import HTTPSConnection
from base64 import b64encode
import json


# Basic set up code 
def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

BASE_URL = "http://localhost:9000"
username = "admin"
password = "admin"

payload = {}
headers = {
  'Authorization': basic_auth(username, password),
  'Content-Type': 'application/json'
  }

def runProcess(process, payload, data, url):
    first_key = list(payload.keys)[0]
    if process == "EDIT":
        returnData = requests.request("GET", url, headers=headers, data=payload)
        for itemsData in returnData:
            if itemsData[first_key] == data[first_key]:
                payload = itemsData

    payload.update(data)
    dic = payload
    payload = json.dumps(dic)
    match process:
        case "GET":
            pros = "GET"
            payload = None
        case "ADD":
            pros = "POST"
        case "REMOVE":
            pros = "DELETE"
            url = url + data["name"].replace(" ", "%20") + "/"
        case "EDIT":
            pros = "PUT"
            
        case default:
            pros = "GET"
            payload = None

    response = requests.request(pros, url, headers=headers, data=payload)

    if response.status_code == 200:
        response = response.json()
        if data.has_key(first_key) and data[first_key] != "":
            for dataItem in response:
                if dataItem[first_key] == data[first_key]:
                    return dataItem
        else:
            return response
    if response.status_code == 201:
        print("New data added succefully")
        return None
    elif response.status_code == 204:
        print(data[first_key] + " deleted from database.")
        return None
    else:
        print('Get data failed:')
        print(response.status_code)
        return None

# Function to change orders 
def ordersIn(process, data):
    url = BASE_URL + "api/input/demand/"
    payload =     {
        "name": "",
        "item": "",
        "location": "",
        "customer": "",
        "due": "",
        "quantity": "",
        "priority": "",
        }
    
    return runProcess(process, payload, data, url)

# Function to change items 
def itemsFunc(process, data):
    url = BASE_URL + "/api/input/item/"
    payload =     {
        "name": "",
        "owner": "All items"
        }
    return runProcess(process, payload, data, url)

# Function to re-run planning algorithm
def runPlan():
    url = BASE_URL + "/execute/api/runplan/"
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print('Get data failed:' + response.status_code)
        return None

# Function to see all factroy locations 
# get all factory locations
def locationFunc(process, data):
    url = BASE_URL + "/api/input/location/"
    payload =     {
        "name": "",
        "owner": "All locations"
        }
    return runProcess(process, payload, data, url)

# Function to look for or edit purchase orders 
# get all orders open, get all orders closed, add delay/change time arrival to set order, add new barcode or reference to order, change order status,
def purchaseOrderFunc(process, data):
    url = BASE_URL + "/api/input/purchaseorder/"
    payload =     {
            "reference": "",
            "quantity": "",
            "item": None,
            "supplier": None,
            "ordering date": None,
            "receipt date": None,
            "location": None,
            "status": None
            }
    runProcess(process, payload, data, url)

# Function to add or edit cusotmers 
# get all cusotmers, add or remove cusotmer 
def customerFunc(process, data):
    url = BASE_URL + "/api/input/customer/"
    payload =     {
        "name": "",
        "owner": "All customers"
        }
    return runProcess(process, payload, data, url)

# Function to add/edit supplier/item supplier or edit exisitng one (including chnaging leadtime)
# get all supplier, edit supplier (lead time, name, cost), edit item supplier (lead time, name, cost), 
def supplierFunc(process, data):
    # data should have name and item or itemsupplir change details
    url = BASE_URL + "/api/input/supplier/"
    url2 = BASE_URL + "/api/input/itemsupplier/"

    #if process is GET then fetch infomation for item supplier (assume they want supplier of item)
    if process == "GET":
        payload = {}
        data["supplier"] = data["name"]
        data.pop("name") 
        return runProcess(process, payload, data, url2)
    elif process == "ADD": #if process is add new supplier also add item supplier
        # check if existing supplier
        datanew ={}
        try:
            datanew["name"] = data["supplier"]
        except:
            datanew["name"] = data["name"]
        response = runProcess("GET", {}, datanew, url)
        if response != None:
            # no exisitng supplier create one and item supplier 
            runProcess("ADD", {}, datanew, url)
            payload = {}
            data["supplier"] = datanew["name"]
            runProcess("ADD",payload, data, url2)
        else:
            data["supplier"] = datanew["name"]
            runProcess("ADD",payload, data, url2)
    elif process == "EDIT":
        # assume item supplier mostly edited
        runProcess("EDIT",{}, data, url2)
    elif process == "DELETE":
        runProcess("DELETE",payload, data, url2)

# Function to edit or get inventory details 
# get all details of inventory avaible now, see inventory predicted for futrue
def inventoryFunc(process, data):
    url = BASE_URL + "/api/input/customer/"
    payload =     {
        "name": "",
        "owner": "All customers"
        }
    return runProcess(process, payload, data, url)

# Function to edit or get inventory buffers needed
# get all buffers currently, edit of change set buffer in inventory


# Function to get manufacturing operation data out to new app view/database 
# get all manufacturing operations in list (name, date start, date end, quantity, parts to make, order number/name), change/delay an operation


# Fucntion to remove machine from operation (all machines must have calendar with "<machine name> working hours")


# Function to change resources 
def resourceFunc(process, data):
    url = BASE_URL + "/api/input/resource/"
    payload =     {
        "name": ""
        }
    return runProcess(process, payload, data, url)

# function to return list of only data from json you want (e.g. names of items, times of deliviery)
def selectKeyData(responseFound, keysIn):
    newData =[]
    if len(responseFound) != 0:
        for response in responseFound:
            data = []
            for k in keysIn:
                data.append(response[k])
            newData.append(data)
        return newData
    else:
        print("Error: no data in to function")
        return None
    

# main python function
if __name__ == "__main__":
    data = ordersIn("GET", {})
    d = data[0]
    #new = ordersIn("Post", d)
    # print(data)
    # process = "GET"
    # inData = {}
    # dataNew = itemsFunc(process, inData)
    #out = runPlan()

    # Edit/add new item
    newData = {"name": "new item"}
    new = itemsFunc("REMOVE", newData)

    print(new)

