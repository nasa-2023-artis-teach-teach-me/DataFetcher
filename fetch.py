import os
import time
import requests
from datetime import datetime, timedelta

with open(".env", "r") as f:

    envs = f.read().split('\n')

    for env in envs:
        key, value = env.split("=")
        os.environ[key] = value

MAP_KEY = os.environ.get("MAP_KEY")
BACKEND = os.environ.get("BACKEND")
DATE_STR= (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d")
URL     = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/world/1/{DATE_STR}"

def check_data():

    r = requests.get(f"{BACKEND}/api/fire/date/{DATE_STR}")

    try:
        r = r.json()['features']
    except:
        return True
    
    have_date = False

    for feature in r:
        
        if feature.get("properties", {'src': "report"}).get('src') == "firm":
            have_date = True
            break

    return have_date

def fetch_data():

    r = requests.get(URL)

    # try:
    #     r = r.json()
    # except:
    #     return False
    
    r = r.text.split('\n')
    results = r[1:]

    for result in results:
        
        r = requests.post(f"{BACKEND}/api/")


if __name__ == "__main__" :

    while check_data():
        time.sleep(10*60)

    fetch_data()