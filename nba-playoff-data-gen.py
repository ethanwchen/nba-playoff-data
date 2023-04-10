#!/usr/bin/env python
# coding: utf-8

# # NBA Playoffs 2023
# 
# Credit goes to nba_api for scraping the data.
# 
# See more here: https://github.com/swar/nba_api

# In[83]:


import pandas as pd
import numpy as np
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandings, leaguegamefinder


# ### The nba_playoffs Dataset
# 
# We fetch a list of all current NBA teams using the get_teams() function from the nba_api package. It then retrieves the current league standings by calling LeagueStandings().get_data_frames()[0]. The get_data_frames() method returns a list of DataFrames, with the first one containing the data of interest which are the current NBA standings.

# In[15]:


# Get all NBA teams
nba_teams = teams.get_teams()

# Get the current league standings
standings = leaguestandings.LeagueStandings().get_data_frames()[0]


# In[37]:


pd_nba_teams = pd.DataFrame(nba_teams)
print(pd_nba_teams.head())
pd_standings = pd.DataFrame(standings)
print(pd_standings.head())
print(standings.columns)


# We then process the NBA team standings data obtained using the leaguestandings module of the nba_api package, and creates a new DataFrame object nba_pos. The nba_pos DataFrame contains the following columns:
# 
# - team: the name of the team
# 
# - team_short: the short name of the team
# 
# - conference: the conference that the team belongs to
# 
# - games_won: the number of games won by the team
# 
# - games_lose: the number of games lost by the team
# 
# - conference_position: the position of the team within its conference
# 
# - games_played: the total number of games played by the team
# 
# - points_scored: the average number of points scored per game by the team
# 
# - points_missed: the average number of points missed per game by the team
# 
# - game_won_home: the number of games won by the team at home
# 
# - game_lose_home: the number of games lost by the team at home
# 
# - game_won_away: the number of games won by the team away
# 
# - game_lose_away: the number of games lost by the team away
# 
# This code also splits the home_record and away_record columns into separate game_won_home, game_lose_home, game_won_away, and game_lose_away columns, and calculates the total number of games played by each team.

# In[48]:


# Create nba_pos DataFrame
nba_pos = standings[['TeamName', 'TeamCity', 'Conference', 'WINS', 'LOSSES', 'ConferenceRecord', 'Record', 'PointsPG', 'OppPointsPG', 'HOME', 'ROAD']].copy()
nba_pos.columns = ['team', 'team_short', 'conference', 'games_won', 'games_lose', 'conference_position', 'games_played', 'points_scored', 'points_missed', 'home_record', 'away_record']

# Split home_record and away_record into separate columns
nba_pos[['game_won_home', 'game_lose_home']] = nba_pos['home_record'].str.split('-', expand=True).astype(int)
nba_pos[['game_won_away', 'game_lose_away']] = nba_pos['away_record'].str.split('-', expand=True).astype(int)

# Drop the original home_record and away_record columns
nba_pos.drop(columns=['home_record', 'away_record'], inplace=True)

# Calculate the total number of games played
nba_pos['games_played'] = nba_pos['game_won_home'] + nba_pos['game_lose_home'] + nba_pos['game_won_away'] + nba_pos['game_lose_away']


# In[34]:


nba_pos


# Now, we create a dictionary playoff_teams which includes the seeds and conference abbreviations of the top 10 teams in the NBA. The code then filters the nba_pos DataFrame to only include the teams in the playoff_teams dictionary. It maps the team abbreviations, seeds, and conference abbreviations to the DataFrame using lambda functions. Finally, the updated nba_pos DataFrame is printed to the console.

# In[49]:


# Update playoff_teams to include seeds and conference abbreviation
playoff_teams = {
    'Nuggets': ('DEN', 1, 'W'), 'Grizzlies': ('MEM', 2, 'W'), 'Kings': ('SAC', 3, 'W'), 'Suns': ('PHX', 4, 'W'), 'Clippers': ('LAC', 5, 'W'), 'Warriors': ('GSW', 6, 'W'), 'Lakers': ('LAL', 7, 'W'), 'Timberwolves': ('MIN', 8, 'W'), 'Pelicans': ('NOP', 9, 'W'), 'Thunder': ('OKC', 10, 'W'),
    'Bucks': ('MIL', 1, 'E'), 'Celtics': ('BOS', 2, 'E'), '76ers': ('PHI', 3, 'E'), 'Cavaliers': ('CLE', 4, 'E'), 'Knicks': ('NYK', 5, 'E'), 'Nets': ('BKN', 6, 'E'), 'Heat': ('MIA', 7, 'E'), 'Hawks': ('ATL', 8, 'E'), 'Raptors': ('TOR', 9, 'E'), 'Bulls': ('CHI', 10, 'E')
}

# Filter nba_pos to show only playoff teams
nba_pos = nba_pos[nba_pos['team'].isin(playoff_teams.keys())]

# Map team abbreviations, seeds, and conference abbreviations to the DataFrame
nba_pos['team_short'] = nba_pos['team'].apply(lambda x: playoff_teams[x][0])
nba_pos['seed'] = nba_pos['team'].apply(lambda x: playoff_teams[x][1])
nba_pos['conf_abbr'] = nba_pos['team'].apply(lambda x: playoff_teams[x][2])

# Print the updated nba_pos DataFrame
nba_pos


# In[50]:


# To CSV
nba_pos.to_csv('nba_playoffs.csv', index=False)


# ### The nba_games Dataset

# In[65]:


from nba_api.stats.static import teams
nba_teams = teams.get_teams()

team_id_mapping = {team['abbreviation']: team['id'] for team in nba_teams}

nba_pos['team_id'] = nba_pos['team_short'].map(team_id_mapping)


# - The code above uses the NBA API to fetch game data and filters the data for the top 10 seeds per conference.
# 
# - The team IDs for the top 10 seeds per conference are obtained from the previously created nba_pos DataFrame.
# 
# - The relevant columns are selected and renamed appropriately.
# 
# - A new DataFrame nba_games is created with the filtered and renamed data.

# In[84]:


# Find team IDs for the top 10 seeds per conference
team_ids = nba_pos['team_id'].tolist()

# Fetch game data using NBA API
gamefinder = leaguegamefinder.LeagueGameFinder()
all_games = gamefinder.get_data_frames()[0]

# Filter for games with the top 10 seeds per conference
nba_games = all_games[all_games['TEAM_ID'].isin(team_ids)]

# Rename and select the necessary columns
nba_games = nba_games.rename(columns={
    'TEAM_NAME': 'team',
    'TEAM_ABBREVIATION': 'team_short',
    'TEAM_ID': 'team_id',
    'GAME_ID': 'matchup_id',
    'PTS': 'points',
    'FG_PCT': 'fg_pct',
    'FT_PCT': 'ft_pct',
    'FG3_PCT': 'fg3_pct'
})

# Keep only the relevant columns
nba_games = nba_games[['team', 'team_short', 'team_id', 'matchup_id', 'points', 'fg_pct', 'ft_pct', 'fg3_pct']]


# This separates NBA games into home and away games, renames columns, merges the two resulting dataframes on the matchup_id column, adds a column for the winning team, and drops unnecessary columns.
# 
# - The home_games dataframe is created by filtering nba_games for games where the matchup contains 'vs.' and the away_games dataframe is created by filtering for games where the matchup contains '@'.
# 
# - The column names in home_games are updated to reflect the fact that they are home games, and the same is done for away_games.
# 
# - The two dataframes are merged on the matchup_id column to create merged_games.
# 
# - The winning_team column is added using numpy.where() to check whether the home team or away team scored more points.
# 
# - Finally, the home_team_id and away_team_id columns are dropped as they are unnecessary for the analysis.

# In[95]:


# Separate home and away games
home_games = nba_games[all_games['MATCHUP'].str.contains('vs.')]
away_games = nba_games[all_games['MATCHUP'].str.contains('@')]

# Rename home and away games columns
home_games = home_games.rename(columns={
    'team': 'home_team',
    'team_short': 'home_team_short',
    'team_id': 'home_team_id',
    'points': 'home_points',
    'fg_pct': 'home_fg_pct',
    'ft_pct': 'home_ft_pct',
    'fg3_pct': 'home_fg3_pct'
})

away_games = away_games.rename(columns={
    'team': 'away_team',
    'team_short': 'away_team_short',
    'team_id': 'away_team_id',
    'points': 'away_points',
    'fg_pct': 'away_fg_pct',
    'ft_pct': 'away_ft_pct',
    'fg3_pct': 'away_fg3_pct'
})

# Merge home_games and away_games DataFrames on 'matchup_id'
merged_games = home_games.merge(away_games, on='matchup_id')

# Add a column for the winning team
merged_games['winning_team'] = np.where(merged_games['home_points'] > merged_games['away_points'], merged_games['home_team_short'], merged_games['away_team_short'])

# Drop unnecessary columns
merged_games.drop(['home_team_id', 'away_team_id'], axis=1, inplace=True)

merged_games.head()


# In[96]:


merged_games.to_csv('nba_games.csv', index=False)

