# NBA-Playoff-Data

<img width="872" alt="Screen Shot 2023-04-09 at 8 05 46 PM" src="https://user-images.githubusercontent.com/96222805/230817377-7af567dc-f880-45b1-86b3-218c37a37bc1.png">

**A script that generates NBA Playoff Data**

This repository provides a dataset of NBA regular season games for the 2021-2022 season. The data is sourced from the NBA API and includes game statistics for all playoff teams.

### Purpose

The purpose of this dataset is to provide NBA fans with data to conduct their own analysis and insights into the 2021-2022 regular season. The dataset includes game statistics such as points scored, field goal percentage, free throw percentage, and three-point field goal percentage.

### Files and Dictionary

#### nba_pos (NBA Standings)

- **team**: The name of the team.

- **team_short**: The abbreviated name of the team.

- **conference**: The conference that the team is in (either "East" or "West").

- **games_won**: The number of games won by the team.

- **games_lose**: The number of games lost by the team.

- **conference_position**: The team's position in their conference standings.

- **games_played**: The total number of games played by the team.

- **points_scored**: The average number of points scored per game by the team.

- **points_missed**: The average number of points missed per game by the team.

- **game_won_home**: The number of games won by the team at home.

- **game_lose_home**: The number of games lost by the team at home.

- **game_won_away**: The number of games won by the team on the road.

- **game_lose_away**: The number of games lost by the team on the road.

- **seed**: The seed of the team in the playoffs (1-10).

- **conf_abbr**: The abbreviation of the conference that the team is in (either "E" or "W").

#### merged_games (NBA Game Results)

- **home_team**: The name of the home team.

- **home_team_short**: The abbreviated name of the home team.

- **home_points**: The number of points scored by the home team.

- **home_fg_pct**: The field goal percentage of the home team.

- **home_ft_pct**: The free throw percentage of the home team.

- **home_fg3_pct**: The three-point field goal percentage of the home team.

- **away_team**: The name of the away team.

- **away_team_short**: The abbreviated name of the away team.

- **matchup_id**: The unique identifier for the game.

- **away_points**: The number of points scored by the away team.

- **away_fg_pct**: The field goal percentage of the away team.

- **away_ft_pct**: The free throw percentage of the away team.

- **away_fg3_pct**: The three-point field goal percentage of the away team.

- **winning_team**: The abbreviated name of the winning team.

### Usage

The dataset can be used for a variety of purposes, including but not limited to:

- Conducting statistical analysis on specific players or teams

- Creating visualizations to better understand trends and patterns in the data

- Building machine learning models to predict game outcomes

## Running the Script

This Python script analyzes the top 10 seeds from each conference of the NBA and predicts the winning team of each matchup. The script uses data from the NBA API and the Pandas library for data manipulation.

### Description of the Code

The script performs the following steps:

- Gets all NBA teams using the nba_api library.

- Retrieves the current league standings using the nba_api library and calculates additional statistics for each team, such as total games played, home and away records, etc.

- Filters the standings to show only the top 10 seeds from each conference.

- Retrieves game data for the top 10 seeds from each conference using the nba_api library.

- Separates the game data into home and away games and merges them into a single DataFrame.

- Adds a column for the winning team and drops unnecessary columns.

- Plots the winning percentage for each team.

### Output

The script outputs a bar chart showing the winning percentage for each team. The chart is saved in the output folder with the name winning_percentage.png.

### License

The dataset is licensed under the MIT License. See the LICENSE file for more information.
