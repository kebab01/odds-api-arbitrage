from pydantic import BaseModel
from datetime import datetime


class Outcome(BaseModel):
    name:str
    price:float

class Market(BaseModel):
    key:str
    last_update:str
    outcomes:list[Outcome]

class Bookmaker(BaseModel):
    key:str
    title:str
    last_update:str
    markets:list[Market]

class Game(BaseModel):
    id: str
    sport_key: str
    sport_title: str
    commence_time: str
    home_team: str
    away_team: str
    bookmakers:list[Bookmaker]

class Action(BaseModel):
    agency:str
    action:Outcome

class BetObject(BaseModel):
    sport_title:str
    commence_time:str
    home_team:str
    away_team:str
    actions:list[Action]
    total_odds:float
    competition:str

class API_KEY_JSON(BaseModel):
    current_index:int
    keys:list[str]