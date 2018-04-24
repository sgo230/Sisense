import requests
import pandas as pd
import json
import re

# Configuration

# Base URL used to access Sisense
sisenseUrl = "http://localhost:8081"

# Path and name for CSV file output
outputPath = "C:\\Users\\Administrator\\Desktop\\Dependencies.csv"

# Either hard-code authorization token or generate new token using admin login credentials
# For more, see: https://developer.sisense.com/display/API2/Using+the+REST+API

authToken = "Bearer {token}" 

#username = "user@example.com"
#password = "MyPassword"

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

def elasticubeDependencies(server, elasticube):

    url = "http://localhost:8081/api/v2/ecm/"

    payload = "{\"query\":\"query getElasticubeDependencies($title: String!, $server: String) {\\n  getElasticubeDependencies(title: $title, server: $server) {\\n    dataSecurity {\\n      exists\\n      __typename\\n    }\\n    buildAlerts {\\n      exists\\n      __typename\\n    }\\n    starredFormulas {\\n      exists\\n      __typename\\n    }\\n    hierarchies {\\n      exists\\n      __typename\\n    }\\n    dashboards {\\n      data {\\n        oid\\n        title\\n        __typename\\n      }\\n      __typename\\n    }\\n    widgets {\\n      data(onlyOrphaned: true) {\\n        oid\\n        title\\n        dashboard {\\n          oid\\n          title\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    pulseKpis {\\n      data {\\n        name\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"," +     "\"variables\":{\"title\":\"" + elasticube + "\",\"server\":\"" + server + "\"}" +     ",\"operationName\":\"getElasticubeDependencies\"}"
    
    headers = {
        'Content-Type': "application/json",
        'Authorization': authToken
        }

    response = requests.request("POST", url, data=payload, headers=headers).json()['data']['getElasticubeDependencies']
    
    return response

def cleanDependencies(server, elasticube, response):
    
    # Handle simple dependencies that exist or do not
    
    df_temp = pd.DataFrame(columns=['Server Name','ElastiCube','Dependency Type','ObjectID','ObjectName'])
    
    booleanDependencies = ['dataSecurity', 'buildAlerts', 'starredFormulas', 'hierarchies']

    for i, dependency in enumerate(booleanDependencies):

        if response[dependency]['exists']:

            append = {"Server Name": server,
                      "ElastiCube": elasticube,
                      "Dependency Type": re.sub(r'([A-Z])', r' \1', booleanDependencies[i]).title()
                     }

            df_temp = df_temp.append(append, ignore_index=True)
            
    if len(response['pulseKpis']['data']) > 0:

        append = {"Server Name": server,
                  "ElastiCube": elasticube,
                  "Dependency Type": "Pulse KPI"}

        df_temp = df_temp.append(append, ignore_index=True)
        
    # Get temporary dataframe of dashboard dependencies and union it to the existing dataframe

    if len(response['dashboards']['data']) > 0:
    
        df_temp_dash = pd.read_json(json.dumps(response['dashboards']['data']))
        df_temp_dash.columns = ['Dependency Type','ObjectID','ObjectName']
        df_temp_dash['Server Name'] = server
        df_temp_dash['ElastiCube'] = elasticube

        df_temp = pd.concat([df_temp, df_temp_dash])
        df_temp = df_temp[['Server Name','ElastiCube','Dependency Type','ObjectID','ObjectName']]
    
    return df_temp

def main():
    
    df = pd.DataFrame(columns=['Server Name','ElastiCube','Dependency Type','ObjectID','ObjectName'])
    
    for server in elasticubeServers():
        for elasticube in serverElasticubes(server):
            df = df.append(cleanDependencies(server, elasticube, elasticubeDependencies(server, elasticube)), 
                           ignore_index=True)
            
    df.to_csv(outputPath, index=False)

authToken = getToken()

if __name__ == '__main__':
    main()