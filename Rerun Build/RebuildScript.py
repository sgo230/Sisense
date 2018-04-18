import requests
import re
import datetime

# Configuration
url_domain = 'http://localhost:8081'
elasticube_server = 'localhost' # ElastiCube server name
elasticube = 'Northwind' # ElastiCube name to build
token = 'Bearer {token}'
# Generate token from instructions at https://developer.sisense.com/display/API2/Using+the+REST+API
build_type = 'Full' # Full: full build
                    # Delta: schema changes
                    # FullUpdateExisting: accumulative
        
build_minutes = 170 # Run build if the last build time exceeds # of minutes ago

if not build_type in ['Full', 'Delta', 'FullUpdateExisting']:
    print("Build type '" + build_type + "' is not valid")
    exit()
	
buildTime_url = url_domain + '/api/elasticubes/servers/' + elasticube_server + '/' + elasticube + '/lastBuildTime'
build_url = url_domain + '/api/elasticubes/' + elasticube_server + '/' + elasticube + '/startBuild?type=' + build_type

response = requests.get(buildTime_url,headers={"Authorization": token})
response = response.json()

last_build_time = datetime.datetime.fromtimestamp(int(re.sub("\D", "", response)) / 1e3)now = datetime.datetime.now()

last_build_minutes_ago = raw_time_diff.days * 24 * 60 + raw_time_diff.seconds / 60
raw_time_diff = now - last_build_time

if last_build_minutes_ago > build_minutes:
    print("Last build time: " + str(last_build_time))
    print("Minutes ago: " + str(int(last_build_minutes_ago)))
    print("Minutes threshold: " + str(build_minutes))
    print("Initiating ElastiCube build of " + elasticube)
    
    requests.post(build_url, headers={"Authorization": token})
    
else:
    print("Last build time: " + str(last_build_time))
    print("Minutes ago: " + str(int(last_build_minutes_ago)))
    print("Minutes threshold: " + str(build_minutes))
    print("ElastiCube build is recent; not initiating build of " + elasticube)