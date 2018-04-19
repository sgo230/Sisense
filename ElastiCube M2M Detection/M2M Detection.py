import requests
import pprint
 
 
# Configuration
 
sisense_url = "http://localhost:8081"
elasticube_server = "localhost"
elasticube = "Northwind"
token = "{token}" # Generate token from steps at https://developer.sisense.com/display/API2/Using+the+REST+API
limit = 0 # Limit the number of records tested; 0 = all records
 
 
# Build headers
headers = {'Authorization': "Bearer " + token}
 
 
# Retrieve list of tables
 
url = sisense_url + "/api/elasticubes/metadata/" + elasticube + "/fields"
response = requests.request("GET", url, headers=headers).json()
 
tables = []
 
for i in range(len(response)):
     
    try:
        if not response[i]['table'] in tables:
            tables.append(response[i]['table'])
    except KeyError:
        pass
 
 
# Retrieve list of relations (joins) for each table
relations = []
 
for table in tables:
 
    url = sisense_url + "/api/v1/elasticubes/" + elasticube_server + "/" + elasticube + "/" + table + "/relations"
    response = requests.request("GET", url, headers=headers).json()['relations']
 
    for i in range(len(response)):
         
        response[i]['sourceTable'] = table
         
    for i in range(len(response)):
         
        tmp = response[i]['sourceTable']
        tmp_response = {}
        tmp_response = dict(response[i])
        tmp_response['sourceTable'] = tmp_response['targetTable']
        tmp_response['targetTable'] = tmp
         
        if tmp_response not in relations: # Exclude converses of existing relations
            relations.append(dict(response[i]))
 
 
def simple_querystring(sourceField,sourceTable,targetField,targetTable,limit):
    '''Generate a SQL query to test the uniqueness of a set of keys
    '''
    query_dict = {}
    query_dict['count'] = limit
    query_dict['query'] = "SELECT DISTINCT_COUNT([" + sourceField + "]) <> COUNT([" + sourceField + "]) FROM [" + sourceTable + "] UNION ALL SELECT DISTINCT_COUNT([" + targetField + "]) <> COUNT([" + targetField + "]) FROM [" + targetTable + "]"
    return query_dict
 
 
url = sisense_url + "/api/elasticubes/" + elasticube + "/Sql"
 
for i in range(len(relations)):
     
    querystring = simple_querystring(relations[i]['sourceField'],
                                     relations[i]['sourceTable'],
                                     relations[i]['targetField'],
                                     relations[i]['targetTable'],
                                     limit)
     
    response = requests.request("GET", url, headers=headers, params=querystring).json()['values']
    relations[i]['M2M'] = response == [['true'],['true']]
 
 
m2m_relations = [i for i in relations if i['M2M'] == True]
 
 
pprint.pprint(m2m_relations)