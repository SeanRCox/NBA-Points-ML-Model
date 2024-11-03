import csv
import time
import os

import pandas as pd
import numpy as nd

from basketball_reference_web_scraper import client as scraper
from basketball_reference_web_scraper.data import OutputType


def create_game_data():
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


get_game_day_data()




def create_player_and_team_data():
    game_days = 1

    years = [2022, 2023, 2024]
    months = [10, 11, 12, 1, 2, 3, 4, 5, 6]
    days = [i for i in range(1, 32)]

    '''
    for year in years:
        for month in months:
            for day in days:
                while(1):
                    try:
                        scraper.player_box_scores(day=day, month=month, year=year,
                                                output_type=OutputType.CSV,
                                                output_file_path=f"data/player_data/day_{game_days}.csv")
                        game_days += 1
                        break
                    except KeyError as e:
                        break # No game on this day
                    except Exception as e:
                        time.sleep(300) # Hit rate limit, sleep

    output_file = open("data/player_stats.csv", 'w')
    writer = csv.writer(output_file)
    for file in [f"data/player_data/day_{i}.csv" for i in range(1, game_days+1)]:
        with open(file, 'r') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                writer.writerow(row)
    '''

    # Now Create the team data

    game_days = 1

    for year in years:
        for month in months:
            for day in days:
                while(1):
                    try:
                        scraper.team_box_scores(day=day, month=month, year=year,
                                                output_type=OutputType.CSV,
                                                output_file_path=f"data/team_data/day_{game_days}.csv")
                        reader = csv.reader(f"data/team_data/day_{game_days}.csv")
                        row_count = sum(1 for row in reader)
                        if row_count == 1: 
                            os.remove(f"data/team_data/day_{game_days}.csv")
                        else:
                            game_days += 1
                        break
                    except KeyError as e:
                        break # No game on this day
                    except Exception as e:
                        print("Sleeping...")
                        time.sleep(300) # Hit rate limit, sleep

    output_file = open("data/team_stats.csv", 'w')
    writer = csv.writer(output_file)
    for file in [f"data/game_data/day_{i}.csv" for i in range(1, game_days+1)]:
        with open(file, 'r') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                writer.writerow(row)

def calculate_drtg():
    pass

def calculate_ppg():
    pass

# Features
# 1: Player IDSs - (1 - n) players (integer)
# 2: Player PPG Average over last 5 games (float)
# 3: Game- Home or Away (1 for home, 0 for away) (integer)
# 4: Opponent DRTG over last 5 games (float)

# Each game, we will get the top 16 players by minutes played
# We get the DRTG and location for the game
# We then look at each players average over the last 5 games leading up to the game,
# which we have already calculated
# We add in the players ID and we have a complete data point
# the target value is the points scored by the player in the game

# Player ID, Game Date, Points Scored
# ->
# Player ID, Game Date, Points Average over last 5 games

# Team ID, Game Date, DRTG
# ->
# Team ID, Game Date, DRTG Average over last 5 games

# Get player/ Team data for each game
# Team datapoints: 
# Date
# Team
# Home/Away
# Calculate DRTG

# Player datapoints
# Date
# Team
# Player ID
# Points