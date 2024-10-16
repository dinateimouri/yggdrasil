#! /bin/bash

# This script is used to run performance tests on the Yggdrasil API
echo "You can also pass the URL of the API as an argument to this script"
echo "The default URL is http://localhost:8080"
echo "Example: ./scripts/performance-test.sh http://localhost:8000"
echo "NOTE: There is no '/' at the end of the URL"
echo ""
echo "---------------------------------------------"
if [ -z "$1" ]; then
  URL=http://localhost:8080
else
  URL=$1
fi

# create a virtual environment and install locust
if [ -d "load-testing/.venv" ]; then
  echo "The required packages are already installed for load testing!"
else
echo "Installing the required packages for load testing"
python3 -m venv load-testing/.venv
load-testing/.venv/bin/pip3 install locust
sleep 5
fi

echo "Running performance tests on the Yggdrasil API"
echo "---------------------------------------------"
echo "Starting the locust server to load end-to-end flow of the Yggdrasil API"
sleep 2
source load-testing/.venv/bin/activate && locust -f load-testing/load_the_llm.py --headless -u 1 -r 1 -t 30s -H $URL

echo "---------------------------------------------"
echo "Starting the locust server to load fastapi validations in the Yggdrasil API"
sleep 2
source load-testing/.venv/bin/activate && locust -f load-testing/load_fastapi_validation.py --headless -u 1 -r 1 -t 30s -H $URL

echo "---------------------------------------------"
echo "Starting the locust server to load a similarity method in the Yggdrasil API"
sleep 2
source load-testing/.venv/bin/activate && locust -f load-testing/load_similarity.py --headless -u 1 -r 1 -t 30s -H $URL


echo "---------------------------------------------"
echo "Starting the locust server to load harmful content detection method in the Yggdrasil API"
sleep 2
source load-testing/.venv/bin/activate && locust -f load-testing/load_harmful_content_detection.py --headless -u 1 -r 1 -t 30s -H $URL
