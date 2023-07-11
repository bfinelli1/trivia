# Trivia

Uses the api from https://jservice.io/

This is a Django app that queries an api and displays jeopardy questions with multiple choice answers. The app also displays a leaderboard for each trivia topic and an individual score area for each user.

TODO:
display correct or incorrect and correct answer - check
have profile page with user's leaderboard - check
disallow duplicate questions - check
disallow duplicate categories - check
try to use postgres - check
try to use docker
try to host on iis

sudo su - postgres
psql

\connect mydb;

Save this answer.

CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

sudo service postgresql start
sudo service postgresql stop
