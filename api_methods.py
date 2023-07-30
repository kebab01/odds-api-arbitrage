import traceback
import requests
from helper_methods import *
from models import *
from dotenv import load_dotenv
import os
import time

BASE_URL="https://api.the-odds-api.com/v4/sports"
key_index=0

def get_games(comp:str) -> list[Game]:
    """
        Returns a list of games
    """
    
    while True:
        load_dotenv()
        "If request fails due to api key qutoa exceeded retry with a new api key"
        region="regions=au"
        bet_format="markets=h2h"
        response=requests.get(f"{BASE_URL}/{comp}/odds?apiKey={os.getenv('ODDS_API_KEY')}&{region}&{bet_format}&dateFormat=iso&oddsFormat=decimal")

        if response.status_code==200:
            games=[Game(**i) for i in response.json()]
            return games
        
        if response.status_code==429:
            time.slee
        elif response.status_code==401:
            #If cant get new key then break out of loop
            try:
                print("API key not valid, retrieving another one")
                global key_index
                key_index=get_new_api_key(key_index)
                continue
            except Exception:
                traceback.print_exc()
                break
        
        raise Exception(f"Getting games request failed for {comp} with status code {response.status_code}: {response.text}")



def get_fav_odd_for_game(game:Game, comp:str) -> list[BetObject]:
    """
    Calculates the best betting combination for a particular game

    Params:
        game: JSON - game to operate on

    return:
        best_bet: JSON - Most favorable bet for that game
    """
    
    try:
        num_of_outcomes=len(game.bookmakers[0].markets[0].outcomes)
    except IndexError:
        return None

    if num_of_outcomes <3:
        pass

    bookie_combinations=cartesian_product(game.bookmakers, num_of_outcomes)
    outcomes:list[BetObject]=[]

    for combination in bookie_combinations:
        actions:list[Action]=[]
        for outcome in range(0, num_of_outcomes):
            actions.append(Action(agency=combination[outcome].key, 
                                  action=combination[outcome].markets[0].outcomes[outcome]))
        
        total_odds=sum([1/i.action.price for i in actions])
        if total_odds<1:
            obj=BetObject(
                competition=comp,
                sport_title=game.sport_title,
                commence_time=game.commence_time,
                home_team=game.home_team,
                away_team=game.away_team,
                actions=actions,
                total_odds=sum([1/i.action.price for i in actions])
            )
            outcomes.append(obj)

    outcomes.sort(key=lambda x: x.total_odds)
    return outcomes
            
def get_fav_odd_for_comp(comp:str) -> list[list[BetObject]]:
    """
    Get the most favorable bet for a game in a particular competition
    """
    try:
        games=get_games(comp)
        if len(games)==0:
            raise Exception(f"No games for {comp}")
    except Exception as e:
        print(e)
        return None

    print(f'received games for {comp}')
    favorable:list[list[BetObject]]=[]
    for i, game in enumerate(games):
        fav=get_fav_odd_for_game(game=game, comp=comp)
        if fav != None and len(fav) != 0:
            favorable.append(fav)

    if len(favorable)==0:
        return None

    # favorable.sort(key=lambda x: x['total_odds'])
    return favorable