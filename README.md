# fetch-nyt-crossword-mini-leaderboard
Collects and stores NYT Mini Crossword leaderboard. Originally derived from Matt Dodge's nyt-crossword-stats [here](https://github.com/mattdodge/nyt-crossword-stats).

This repository takes Matt's code a step further by 1) going into more detail around how to uncover which NYT API to connect to and 2) collecting NYT mini crossword leaderboard stats rather than the daily score of your full crossword. I would recommend viewing his repository before checking this out, as he may mention some details that I will not here. 

## Usage
Pulls a snapshot of the current NYT Mini Crossword leaderboard and saves a `csv` in the path provided. 
`python fetch_leaderboard_stats.py -u yourNYTemail -p yourNYTpassword -w yourworkingdirectory`

The file will be named `crossword_stats_yyyy_mm_dd.csv`

## Data Fields

**name**: name of participant
<br>
**score.secondsSpentSolving**: seconds (in whole numbers) taken to complete the crossword
<br>
**date**: date in which data was collected. NOTE this may **not** be the date of the Mini Crossword, as it resets at 10pm EST. 
<br>
**rank**: rank (1 = fastest time) relative to others on the leaderboard
<br>
**points**: inverse of rank, where the fastest time gets the number of points of those on the leaderboard. 

## Example Data
```
,name,score.secondsSpentSolving,date,rank,points
0,user1,43.0,2021-04-26,1,5
1,user2,51.0,2021-04-26,2,4
2,user3,67.0,2021-04-26,3,3
3,user4,113.0,2021-04-26,4,2
4,user5,142.0,2021-04-26,5,1
```
