import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

"""
Data:

Note: Only players who have played atleast 5 games in the NBA 
over the last 3 seasons are included in the data.

X: 

Player_IDs (1-729) : Unique ID associated with the player, 

Team_IDs (1-30) : Unique ID associated with the player's current team

PPG/5 : The player's average points scored over the last 5 games played

Location : 1 for Home, 0 for away

y:

points: the amount of points scored by the player in the given game
"""

data = pd.read_csv('data/training_data.csv')

X = data[['player_id', 'team_id', 'ppg/5', 'location']]
y = data[['points']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
MAE = mean_absolute_error(y_test, predictions)

print(MAE) # MAE = 4.812619023659505

