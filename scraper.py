import csv
import time
import pandas as pd

from basketball_reference_web_scraper.basketball_reference_web_scraper import client as scraper
from basketball_reference_web_scraper.basketball_reference_web_scraper.data import OutputType
 
def get_game_data():
    """
    Get data for every game played in the last 3 seasons.
    """
    for season in [2024]:
        scraper.season_schedule(season_end_year=season, output_type=OutputType.CSV, 
                                output_file_path="data/{}_data.csv".format(season))

    combined_file = open("data/game_data.csv", 'w')
    writer = csv.writer(combined_file)
    for file in ["data/2022_data.csv", "data/2023_data.csv", "data/2024_data.csv"]:
        with open(file, 'r') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                writer.writerow(row)

def get_game_day_data():
    """
    Get every date on which an NBA game was played in the last 3 seasons.
    """
    game_days = []
    games = pd.read_csv("data/game_data.csv")
    for i, row in games.iterrows():
        date = (row["start_time"][0:4], 
                          row["start_time"][5:7], 
                          row["start_time"][8:10])
        if date not in game_days:
            game_days.append(date)

    game_day_df = pd.DataFrame(game_days)
    game_day_df.to_csv("data/game_day_data.csv", index=False)

def get_player_data():
    """
    Get the player data for each game day.
    """
    game_dates = []
    file = "data/game_day_data.csv"
    with open(file, 'r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            game_dates.append(row)

    game_days = 1

    for game in game_dates:
        while(1):
            try:
                print(f"Getting Game Data for {game[2]}-{game[1]}-{game[0]}")
                scraper.player_box_scores(day=game[2], month=game[1], year=game[0],
                                        output_type=OutputType.CSV,
                                        output_file_path=f"data/player_data/day_{game_days}.csv")
                game_days += 1
                break
            except KeyError as e:
                break # No game on this day
            except Exception as e:
                print("Sleeping...")
                time.sleep(300) # Hit rate limit, sleep

    output_file = open("data/player_stats.csv", 'w')
    writer = csv.writer(output_file)
    for file in [f"data/player_data/day_{i}.csv" for i in range(1, game_days+1)]:
        with open(file, 'r') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                writer.writerow(row)

def calculate_ppg():
    """
    Calculate the average ppg/5 for each training example
    """
    stats = pd.read_csv("data/sorted_stats.csv")
    grouped_stats = stats.groupby('name')
    grouped_dfs = {}
    for group_name, group_df in grouped_stats:
        grouped_dfs[group_name] = group_df

    new_dfs = []
    for g in grouped_dfs.values():
        if g.shape[0] <= 5:
            continue
            # skip all players with 5 or fewer games played

        for i in range(5, g.shape[0]):
            last_five = sum([g.iloc[j]['points'] for j in range(i-5, i)]) / 5
            g.loc[g.index[i], 'ppg_over_last_five'] = last_five

        g = g.drop(g.index[:5])

        new_dfs.append(g)

    merged_df = pd.concat(new_dfs, axis=0, ignore_index=True)
    merged_df.to_csv("data/final_player_stats.csv", index=False)

def numerical_representation():
    """
    Convert the categorical data (names, teams, home/away) 
    into numerical representations
    """
    stats = pd.read_csv("data/final_player_stats.csv")
    player_list = list(stats['name'].unique())
    team_list = list(stats['team'].unique())

    output_file = open("data/final_stats.csv", 'w')
    writer = csv.writer(output_file)
    with open('data/final_player_stats.csv', 'r') as input_file:
        reader = csv.reader(input_file)

        skip = True
        for row in reader:
            if skip: 
                skip = False
                continue

            row[0] = player_list.index(row[0])+1
            row[1] = team_list.index(row[1])+1
            row[2] = 1 if row[2] == 'HOME' else 0
            row.pop(4)
            
            writer.writerow(row)

def shuffle_data():
    """
    Shuffle the data
    """
    data = pd.read_csv('data/final_stats.csv')
    shuffled_data = data.sample(frac=1)
    shuffled_data.to_csv('data/training_data.csv', index=False)
        

    

