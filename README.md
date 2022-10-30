# Trivia

Uses the api from https://jservice.io/

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

For same error I did something different, well not different but I directly went to psql server(in my case). It happend during the development. So, I was not concious about possible data losses. Select your database. Then, create schema.

CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

sudo service postgresql start
sudo service postgresql stop
