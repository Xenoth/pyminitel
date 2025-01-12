import requests, json
import time

root_url = "https://api.helldivers2.dev"
api_v1 = '/api/v1/'
api_raw = '/raw/api/'

class PlanetStatus():
        def __init__(self, name: str, owner: str, percentage: float, players: int, attacking: bool) -> None:
            self.name = name
            self.owner = owner
            self.percentage = percentage
            self.players = players
            self.attacking = 'attacking' if attacking else 'defending'

        def is_defence(self) -> bool :
            return self.owner == "Humans"

class WarStatus():

    def get_api_data(url):
        while(1):
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                return data
            except requests.exceptions.RequestException as e:
                if response.status_code == 429:
                    retry_time = int(response.headers['retry-after'])
                    print('429 got - retry time: ' + str(retry_time))
                    time.sleep(int(response.headers['retry-after']))
                else:
                    return None
            

    def geCurrentWarID() -> str :
        api_url = root_url + api_raw + 'WarSeason/current/WarID'
        return WarStatus.get_api_data(api_url)['id']

    def getWarInfo(war_id: str):
        api_url = root_url + api_raw + str(war_id) + '/status'
        return WarStatus.get_api_data(api_url)


    def getWarMajorOrder():
        api_url = root_url + api_v1 + 'assignments'
        res = []
        assignements = WarStatus.get_api_data(api_url)
        for assignement in assignements:
            res.append(assignement['briefing'])

        return res


    def getWarFeeds():
        api_url = root_url + api_v1 + 'dispatches'
        res = []
        feeds = WarStatus.get_api_data(api_url)
        for feed in feeds:
            res.append(feed['message'])

        return res

    def getPlanetsCampaigns():
        api_url = root_url + api_v1 + 'campaigns'
        planets = []
        campaigns = WarStatus.get_api_data(api_url)
        for campaign in campaigns:

            planet = campaign['planet']
            planet_id = planet['index']

            api_url = root_url +  api_v1 + 'planets/' + str(planet_id)
            api_data = WarStatus.get_api_data(api_url)
            
            planets.append(PlanetStatus(
                api_data['name'],
                api_data['currentOwner'],
                (api_data['health'] / api_data['maxHealth'])  * 100,
                api_data['statistics']['playerCount'],
                'attacking' in api_data['statistics']
            ))

        return planets
    
    def __init__(self) -> None:
        self.war_id = WarStatus.geCurrentWarID()
        self.feeds = WarStatus.getWarFeeds()
        self.major_order = WarStatus.getWarMajorOrder()
        self.planets = WarStatus.getPlanetsCampaigns()

war = WarStatus()
print(war)