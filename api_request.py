import configparser
import requests

# Development key changes every 24 hours, access it by logging in to the Riot Developer Portal with your League of Legends account
config = configparser.ConfigParser()
config.read('config.cfg')
api_key = config["AUTH"]["RIOT_API_KEY"]

# request headers
headers = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": api_key,
    "Accept-Language": "en-us",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
}


def winrate(wins, losses):
    """
    Given number of wins and losses, calculate the winrate as a percentage
    """
    return wins / (wins + losses) * 100


def getMatchList(summonerId: str, routing):
    params = f'?type=ranked&count=100'
    summonerMatchlistUrl = f'https://{routing}.api.riotgames.com/lol/match/v5/matches/by-puuid/{summonerId}/ids{params}'
    res = requests.get(summonerMatchlistUrl, headers=headers).json()
    return res


def displayWinrates(summonerId, matchList: list, routing, target_champion):
  """
  Iterates through matchlist, prints out results and returns list of
  champions played, and a list of their corresponding winrates
  """
  wins, losses = (0, 0)
  champion_winrates = {}

  # Parse through matchlist
  for matchId in matchList:

      # Access match data
      matchUrl = f'https://{routing}.api.riotgames.com/lol/match/v5/matches/{matchId}'
      matchInfo = requests.get(matchUrl, headers=headers).json()["info"]

      for player in matchInfo["participants"]:
          if player["puuid"] == summonerId:
              win = player["win"]
              champion = player["championName"]
              break

      # Increments win/loss counters for overall and per champion
      if win:
          wins += 1
          if champion in champion_winrates:
              champion_winrates[champion][0] += 1
          else:
              champion_winrates[champion] = [1, 0, 0]
      else:
          losses += 1
          if champion in champion_winrates:
              champion_winrates[champion][1] += 1
          else:
              champion_winrates[champion] = [0, 1, 0]
      champion_winrates[champion][2] += 1

  # Sort champions in descending order of games
  champion_winrates = dict(
      sorted(champion_winrates.items(), reverse=True, key=lambda x: x[1][2]))
  champion_list = []
  champion_winrates_list = []

  print(champion_winrates)

  # Overall wins and losses
  print(wins, 'wins', losses, 'losses')

  # Overall winrate to two decimal places
  print('%.2f' % (winrate(wins, losses)) + "%")

  print(target_champion)
  percentage = (winrate(
      champion_winrates[target_champion][0], champion_winrates[target_champion][1]))
  games = champion_winrates[champion][2]
  print(percentage)
  print(games)

  return percentage, games
