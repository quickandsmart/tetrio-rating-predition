![image](https://user-images.githubusercontent.com/52612115/231041991-bbb2fd36-b6ce-4e87-b5c4-b2b9e9dcd4c2.png)

# Tetra League TR Prediction

## Project Description

The Project is meant to be a prediction model for a player's Tetra Rating (TR) on the popular web browser game Tetr.io. I used the Tetr.io api to grab the current Tetra League leaderboard which contained stats such as a player's current rating, their PPS (pieces per second), their best rank, etc. I then trained several models with the dataset, using the sklearn package and specifically the Linear Regression, Lasso, and Decision Tree Regressors to find which one worked the best. I then created a python flask server to host the model and a website to easily run predictions from. 

## Overview of Tetr.io and Tetra League

Tetr.io is a block stacking game similiar to that of Tetris Effect Connected, except without the speed limit. Tetra League is a competitive ranked gamemode where you 1v1 against other players and beat them to gain rating and climb up the leaderboard. Some important statistics used in my model to determine a player's skill is APM and PPS. APM stands for Attack per Minute and is how many the average amount of lines you send your opponent with attacks in a minute. PPS stands for Pieces Per Second and is the average amount of pieces you place on your board per second. The APM and PPS can vary greately depending on the rank of the player so they are two of the many useful statistics the models I used to determine a player's rating. These prediction models can be useful as they can help determine if a person is underrated, overrated, or properly rated given their current stats and may help a player better determine how they will do against their opponent.

## Dependencies and How to Run 

Once you've downloaded the files first make sure you have the correct package versions. To do so open up the command prompt and move the **'server'** directory, then run the command **'pip install -r requirements.txt'** and wait for all of the packages to finish installing. Then you should be able to run the command 'python server.py' which will start running the local flask server for you. After that, open up the **'client'** folder and open up the app.html file. This should open up a website for you to do your predictions. Just enter any player who has played at least ten games of tetra league and it will give their predicted TR and actual tr. You can find a list of most active players here https://ch.tetr.io/players/

## Future Work

I plan on trying more models such as random forest to see if they can handle outliers even better than the current models I use. I will also add additional quality of life features on the website such as letting the user know when the account they're trying to predict doesn't exist or hasn't played Tetra league and proving the players current Tetra League stats .
