import numpy as np
import pandas as pd
from collections import Counter
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def win_pct(year, kd=True):
    '''win_pct(2019, kd=False) >> 0.75
    By default, kd=True means with KD healthy'''
    # clean data
    # regular season
    year=2019
    data = pd.read_csv(f'./6_ab_kd/{year}.txt', sep=',')
    new_columns = ['Rk', 'G', 'Date', 'Age', 'Tm', 'Away', 'Opp', 'Result', 'GS',
       'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-']
    data.columns=new_columns
    # replace did not dress with inactive
    data.GS = np.where(data.GS == 'Did Not Dress','Inactive',data.GS)
    if kd == False:
        game_logs = list(data[data.GS=='Inactive'].Result)
    else:
        game_logs = list(data[data.GS!='Inactive'].Result)
    results = Counter([game.split(' ')[0] for game in game_logs])

    try:
        win_pct = results['W']/(results['W']+results['L'])
        return win_pct, results
    except:
        return 1.0, {'W': 0, 'L':0}

# play offs vs regular season is a different beast, going to keep it separate
win_pct('2019', kd=True)
win_pct('2019', kd=False)

# 7 of 11 with KD
win_pct('2019_playoffs', kd=True)
# 6 of 9 without KD, skewed by Portland Series. Much needed for Toronto.
win_pct('2019_playoffs', kd=False)

win_pct('2018', kd=True)
win_pct('2018', kd=False)

win_pct('2018_playoffs', kd=True)
win_pct('2018_playoffs', kd=False)

win_pct('2017', kd=True)
win_pct('2017', kd=False)

win_pct('2017_playoffs', kd=True)
# Only lost 1 game in the Finals
win_pct('2017_playoffs', kd=False)
# Unfair, against first round

# combine all all regular season
def win_pct_reg_season(kd=True):
    '''win_pct_reg_season(kd=True) >> 0.74 '''
    wins = win_pct('2019', kd=kd)[1]['W']+win_pct('2018', kd=kd)[1]['W']+win_pct('2017', kd=kd)[1]['W']
    losses = win_pct('2019', kd=kd)[1]['L']+win_pct('2018', kd=kd)[1]['L']+win_pct('2017', kd=kd)[1]['L']
    return wins/(wins+losses)

win_pct_reg_season(kd=True)
win_pct_reg_season(kd=False)
# Worse without Durant

# combine all playoffs
def win_pct_playoffs(kd=True):
    '''win_pct_playoffs(kd=True) >> 0.79'''
    wins = win_pct('2019_playoffs', kd=kd)[1]['W']+win_pct('2018_playoffs', kd=kd)[1]['W']+win_pct('2017_playoffs', kd=kd)[1]['W']
    losses = win_pct('2019_playoffs', kd=kd)[1]['L']+win_pct('2018_playoffs', kd=kd)[1]['L']+win_pct('2017_playoffs', kd=kd)[1]['L']
    return wins/(wins+losses)

win_pct('2019_playoffs', kd=False)
win_pct('2018_playoffs', kd=False)
win_pct('2017_playoffs', kd=False)

win_pct_playoffs(kd=True)
win_pct_playoffs(kd=False)

# get observed data
data = pd.read_csv(f'./6_ab_kd/2019.txt', sep=',')
new_columns = ['Rk', 'G', 'Date', 'Age', 'Tm', 'Away', 'Opp', 'Result', 'GS',
   'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB',
   'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-']
data.columns=new_columns
game_logs = data.Result
results = [game.split(' ')[0] for game in game_logs]
occurences = [1 if result == 'W' else 0 for result in results]
