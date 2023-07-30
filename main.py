import traceback
from api_methods import *
from helper_methods import *
import logging
import asyncio

logging.basicConfig(filename="data.log", level=logging.NOTSET, format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

async def get_and_append_odds(comp, sport_odds):
    try:
        odds_for_comp = await asyncio.to_thread(get_fav_odd_for_comp, comp)
        if odds_for_comp is not None:
            for i in odds_for_comp:
                for x in i:
                    sport_odds.append(x)
    except Exception as e:
        traceback.print_exc()

async def find_opportunities():

    competitions=load_comps()
    logging.info(f"finding opportunities in {len(competitions)} competitions")

    sport_odds:list[BetObject]=[]
    tasks=[]

    print("starting requests")
    for comp in competitions:
        task = asyncio.create_task(get_and_append_odds(comp, sport_odds))
        tasks.append(task)

    await asyncio.gather(*tasks)
    print("finished requests")

    sport_odds.sort(key=lambda x: x.total_odds)
    write_to_excel(sport_odds)

    with open("opportunities.json",'w') as f:
        json.dump([item.model_dump() for item in sport_odds], fp=f)

def test():
    pass

if __name__ == "__main__":
    # asyncio.run(find_opportunities())
    test()
    