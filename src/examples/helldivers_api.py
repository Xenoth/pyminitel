import requests, datetime
import time

from logging import log, ERROR, WARNING

root_url = "https://api.helldivers2.dev"
api_v1 = '/api/v1/'
api_v2 = '/api/v2/'
api_raw = '/raw/api/'

class PlanetStatus():
        def __init__(self, name: str, owner: str, percentage: float, players: int, faction: str, end_time: str) -> None:
            self.name = name
            self.owner = owner
            self.percentage = percentage
            self.players = players
            self.faction = faction
            self.end_time = end_time

        def is_defence(self) -> bool :
            return self.owner == "Humans"

class WarStatus():

    def get_api_data(url):
        while(1):
            try:
                print(url)

                response = requests.get(url, headers={'X-Super-Client': 'minitel.xenoth.fr', 'X-Super-Contact': 'xenothvalack@gmail.com'})
                response.raise_for_status()
                data = response.json()

                return data
            except requests.exceptions.RequestException as e:
                if response.status_code == 429:
                    retry_time = int(response.headers['retry-after'])
                    log(WARNING, 'Request response 429 - retry time: ' + str(retry_time))
                    time.sleep(int(response.headers['retry-after']))
                else:
                    log(ERROR, 'Got Request exception (' + str(response.status_code) + ')')

                    return None
            

    def geCurrentWarID() -> str :
        api_url = root_url + api_raw + 'WarSeason/current/WarID'
        return WarStatus.get_api_data(api_url)['id']

    def getWarInfo(war_id: str):
        api_url = root_url + api_raw + str(war_id) + '/status'
        return WarStatus.get_api_data(api_url)


    def getWarMajorOrder():
        api_url = root_url + api_v1 + 'assignments'

        assignements = WarStatus.get_api_data(api_url)
        major_order = assignements[0]['briefing']

        print(major_order)

        # summarizator = pipeline("summarization", model="t5-small", tokenizer="t5-small")
        # summar = summarizator(major_order, max_length=15, min_length=10, do_sample=True)[0]['summary_text']
        # print(summar)
        return major_order

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

            percentage = ((planet['maxHealth'] - planet['health']) / planet['maxHealth'])  * 100
            faction = planet['currentOwner']
            end_time = None

            if planet['event']:
                percentage = ((planet['event']['maxHealth'] - planet['event']['health']) / planet['event']['maxHealth'])  * 100
                faction = planet['event']['faction']
                end_time = planet['event']['endTime']
            
            planets.append(PlanetStatus(
                planet['name'],
                planet['currentOwner'],
                percentage,
                planet['statistics']['playerCount'],
                faction = faction,
                end_time=end_time
            ))

        planets.sort(key=lambda x: x.players, reverse=True)
        return planets
    
    def __init__(self) -> None:
        self.war_id = WarStatus.geCurrentWarID()
        self.feeds = WarStatus.getWarFeeds()
        self.major_order = WarStatus.getWarMajorOrder()
        self.planets = WarStatus.getPlanetsCampaigns()
        self.date = datetime.datetime.now()