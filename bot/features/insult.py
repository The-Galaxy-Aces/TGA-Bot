import requests
import html


class Insult:
    def __init__(self):
        #TODO: allow for a variety of insults from different APIs
        #TODO: ADD: https://insult.mattbas.org/api

        self.uri = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        self.insult = ""

    def generateInsult(self):
        resp = requests.get(self.uri)
        if resp.status_code == 200:
            self.insult = resp.json()["insult"]
        else:
            raise Exception(
                "Insult.generate_insult: Error in request: Status Code!=200")

    def getInsult(self):
        self.generateInsult()
        return html.unescape(self.insult)
