import requests
import pandas as pd
import json

# Configuration

sisenseUrl = "http://localhost:8081" # Base URL used to access Sisense
outputPath = "C:\\Users\\{user}\\Desktop\\ElastiCubes.csv" # Path and name for CSV file output

#Either hard-code authorization token or generate new token using admin login credentials

#authToken = "Bearer {token}" # https://developer.sisense.com/display/API2/Using+the+REST+API

username = "example@user.com"
password = "MyPassword123"

# Sisense versions 7.0+ store some user/session metadata for the ECM 2.0 ("Data" tab) feature
# This data is stored in a hidden ElastiCube table named "users"
# Set this value to False if you have a table exactly named users (otherwise it will be deleted from the output)

dropusersTable = True

def getToken():
    try:
        return authToken
    
    except NameError:
        
        url = sisenseUrl + "/api/v1/authentication/login"

        payload = "username=" + username + "&password=" + password
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
            }

        response = requests.request("POST", url, data=payload, headers=headers).json()['access_token']

        return "Bearer " + response

def elasticubeServers():

    url = sisenseUrl + "/api/elasticubes/servers"

    headers = {
        'Authorization': authToken
        }

    response = requests.request("GET", url, headers=headers).json()
    
    return [server['address'] for server in response]

def serverElasticubes(server):
    
    url = sisenseUrl + "/api/elasticubes/servers/" + server
    
    headers = {
        'Authorization': authToken
        }

    response = requests.request("GET", url, headers=headers).json()

    for i in range(len(response)):
        response[i]['elasticubeServer'] = server
        
    return [cube['title'] for cube in response]
	
def elasticubeMetadata(server, elasticube):

    url = sisenseUrl + "/api/datasources/" + server + "/" + elasticube + "/fields/search"

    payload = '{"offset":0,"count":0}'
    headers = {
        'Authorization': authToken,
        'Content-Type': "application/json"
        }

    response = requests.request("POST", url, data=payload, headers=headers).json()
    
    for i in range(len(response)):
        response[i]['elasticubeServer'] = server
        response[i]['elasticube'] = elasticube
    
    return response

def compileMetaData():
    elasticubes = []
    for server in elasticubeServers():
        for elasticube in serverElasticubes(server):
            elasticubes.extend(elasticubeMetadata(server, elasticube))
    return elasticubes

def main():
    df = pd.read_json(json.dumps(compileMetaData()))

    df = df[['elasticubeServer','elasticube','table','title','dimtype']].dropna()

    if dropusersTable:
        df = df[df['table'] != 'users']

    df.columns = ['Server', 'ElastiCube', 'Table', 'Field', 'Data Type']

    df.to_csv(outputPath, index=False)

authToken = getToken()

if __name__ == '__main__':
    main()

