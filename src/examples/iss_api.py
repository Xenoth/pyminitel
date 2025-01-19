import requests

from logging import log, ERROR



class ISS():
        def __init__(self, timestamp: float, latitude: float, longitude: str) -> None:
            self.timestamp = timestamp
            self.latitude = latitude
            self.longitude = longitude

class ISS_API():

    URL = "http://api.open-notify.org/iss-now.json"

    def getISS() -> ISS:
        while(1):
            try:
                response = requests.get(ISS_API.URL, headers={'X-Super-Client': 'minitel.xenoth.fr', 'X-Super-Contact': 'xenothvalack@gmail.com'})
                response.raise_for_status()
                data = response.json()

                response = requests.get("http://api.open-notify.org/iss-now.json")
                data = response.json()

                if data["message"] == "success":
                    return ISS(timestamp=int(data["timestamp"]), latitude=float(data["iss_position"]["latitude"]),longitude=float(data["iss_position"]["longitude"]))
                else:
                    log(ERROR, 'Request failed (' + str(data["message"] == "success") + ')')
                return data
            
            except requests.exceptions.RequestException as e:
                log(ERROR, 'Got Request exception (' + str(response.status_code) + ')')

                return None
            

    
    def __init__(self) -> None:
        pass