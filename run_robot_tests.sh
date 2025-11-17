#!/bin/bash

echo "Running tests"

# luodaan tietokanta
poetry run python src/db_helper.py

echo "DB setup done"

# käynnistetään Flask-palvelin taustalle
poetry run python3 src/index.py &

echo "started Flask server"

# odetetaan, että palvelin on valmiina ottamaan vastaan pyyntöjä
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5000)" != "200" ]];
  do sleep 1;
done

echo "Flask server is ready"

# suoritetaan testit
# The tests are located under src/story_tests.py (directory named with .py suffix),
# so point Robot to that path.
poetry run robot --variable HEADLESS:true src/story_tests

status=$?

# pysäytetään Flask-palvelin portissa 5000
kill $(lsof -t -i:5000)

exit $status