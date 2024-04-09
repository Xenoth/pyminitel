import requests, json

class PlanetStatus():
        def __init__(self, name: str, owner: str, percentage: float, players: int, faction: str) -> None:
            self.name = name
            self.owner = owner
            self.percentage = percentage
            self.players = players
            self.faction = faction

        def is_defence(self) -> bool :
            return self.owner == "Humans"

class WarStatus():

    def get_api_data(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def geCurrentWarID() -> str :
        api_url = 'https://helldivers-2.fly.dev/api'
        return WarStatus.get_api_data(api_url)['current']

    def getWarInfo(war_id: str):
        api_url = 'https://helldivers-2.fly.dev/api/' + war_id + '/status'
        return WarStatus.get_api_data(api_url)


    def getWarMajorOrder(war_info, lang='fr'):
        return war_info['global_events'][0]['message'][lang]

    def getWarFeeds(war_id):
        api_url = 'https://helldivers-2.fly.dev/api/' + war_id + '/feed'
        res = []
        feeds = WarStatus.get_api_data(api_url)
        for feed in feeds:
            res.append(feed['message']['fr'])

        return res

    def getPlanetsCampaigns(war_id, war_info):
        campaigns = war_info['campaigns']
        planets = []
        for campaign in campaigns:

            planet = campaign['planet']
            planet_id = planet['index']

            api_url = 'https://helldivers-2.fly.dev/api/' + str(war_id) + '/planets/' + str(planet_id) + '/status'
            api_data = WarStatus.get_api_data(api_url)
            
            planets.append(PlanetStatus(
                api_data['planet']['name'],
                api_data['owner'],
                api_data['liberation'],
                api_data['players'],
                'None'
            ))

        return planets
    
    def __init__(self) -> None:
        self.war_id = WarStatus.geCurrentWarID()
        self.feeds = WarStatus.getWarFeeds(self.war_id)
        self.war_info = WarStatus.getWarInfo(war_id=self.war_id)
        self.major_order = WarStatus.getWarMajorOrder(self.war_info)
        self.planets = WarStatus.getPlanetsCampaigns(self.war_id, self.war_info)
