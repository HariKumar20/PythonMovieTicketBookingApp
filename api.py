import requests
import json 

def getAPIDataByKey(key):
    try :
        with open('data.json') as file:
            data = json.load(file) 
    except FileNotFoundError:
        print("File not Found") 
    except json.JSONDecodeError:
        print("Invalid Data") 
    else:
        users = data.get(key) 
    return users 

def getAPIFullData():
    with open('data.json') as file:
        data = json.load(file) 
    return data 

def postApiData(ApiData):
    with open('data.json','w') as file:
        json.dump(ApiData,file)