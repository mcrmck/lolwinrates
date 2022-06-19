import api_request as api
import urllib.parse


REGIONS = {
    "br": "br1",
    "eune": "eun1",
    "euw": "euw1",
    "jp": "jp1",
    "kr": "kr",
    "lan": "la1",
    "las": "la2",
    "na": "na1",
    "oce": "oc1",
    "tr": "tr1",
    "ru": "ru"
}

# Queue codes:
# 400 - 5v5 Draft Pick
# 420 - 5v5 Ranked Solo
# 430 - 5v5 Blind Pick
# 440 - 5v5 Ranked Flex
# 450 - 5v5 ARAM
QUEUES = {
    'draft': 400,
    'solo': 420,
    'blind': 430,
    'flex': 440,
    'aram': 450
}


def routingSelector(region):
    """
    Match history data uses routing regions instead
    """
    if region in ["na", "br", "lan", "las", "oce"]:
        return "americas"
    if region in ["kr", "jp"]:
        return "asia"
    if region in ["eune", "euw", "tr", "ru"]:
        return "europe"
    assert False, "not matched"


def run(request):
  # If testing locally, comment the following out
  if request.method == 'OPTIONS':
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }
    return ('', 204, headers)

  headers = {
      'Access-Control-Allow-Origin': '*'
  }

  routing = routingSelector('euw')

  # Gets list of champions & their winrates as a pair of lists, in order of number of games played
  puuid = request.args.get('puuid')
  champion = urllib.parse.unquote_plus(request.args.get('champion'))

  matchlist = api.getMatchList(puuid, routing)
  print(matchlist)
  x, y = api.displayWinrates(puuid, matchlist, routing, champion)
