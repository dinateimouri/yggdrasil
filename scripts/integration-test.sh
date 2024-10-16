#! /bin/bash

# This script is used to run integration tests on the API
echo "You can also pass the URL of the API as an argument to this script"
echo "The default URL is http://localhost:8080"
echo "Example: ./scripts/integration-test.sh http://localhost:8000"
echo "NOTE: There is no '/' at the end of the URL"
echo ""
echo "Running integration tests on the Yggdrasil API"
echo "---------------------------------------------"
if [ -z "$1" ]; then
  URL=http://localhost:8080
else
  URL=$1
fi

# print function
print_output () {
  check_mark=$(python3 -c 'print("\u2705")')
  cross_mark=$(python3 -c 'print("\u274C")')
  if [[ $1 -eq $3 ]]; then
    # GREEN='\033[0;32m'
    # RED='\033[0;31m'

    echo "Test scenario '"$2"' passed! $check_mark"
  else
    echo "Test scenario '"$2"' failed! $cross_mark"
  fi
}

test_func () {
  if [[ $3 -eq 'llm' ]]; then
    response=$(curl -X POST -s $1 -d "$4" -H 'Content-Type: application/json' -H 'accept: application/json')
    if [[ $response == *"$5"* ]]; then
      response_code=$3
    else
      response_code="fail"
    fi

  else
    if [ -z "$4" ]; then
        response_code=$(curl -s -o /dev/null -w "%{http_code}" $1)
    else
        response_code=$(curl -X POST -s -o /dev/null -w "%{http_code}" $1 -d "$4" -H 'Content-Type: application/json' -H 'accept: application/json' )
    fi
  fi
  print_output $response_code "$2" $3
}

test_func $URL/healthz "Get /healthz" 200

test_func $URL/health "Get /health" 404

test_func $URL/sync-chat "Post /sync-chat with complete data" 200 '{"prompts": ["string", "string"], "similarity_measure": "cosine"}'

test_func $URL/sync-chat "Post /sync-chat with response from llm" "llm" '{"prompts": ["string", "string"], "similarity_measure": "cosine"}' "response"

test_func $URL/sync-chat "Post /sync-chat with invalid similarity method" 422 '{"prompts": ["string", "string"], "similarity_measure": "invalid"}'

test_func $URL/sync-chat "Post /sync-chat with no similarity method" 200 '{"prompts": ["string", "string"]}'

test_func $URL/sync-chat "Post /sync-chat with no prompts" 422 '{"prompts": [], "similarity_measure": "cosine"}'

test_func $URL/sync-chat "Post /sync-chat with one prompt" 422 '{"prompts": ["string"], "similarity_measure": "cosine"}'

test_func $URL/sync-chat "Post /sync-chat with no similar prompt" 400 '{"prompts": ["string1", "string2"], "similarity_measure": "cosine"}'

test_func $URL/sync-chat "Post /sync-chat with cosine method" 200 '{"prompts": ["string", "string"], "similarity_measure": "cosine"}'

test_func $URL/sync-chat "Post /sync-chat with euclidean method" 200 '{"prompts": ["string", "string"], "similarity_measure": "euclidean"}'

test_func $URL/sync-chat "Post /sync-chat with manhattan method" 200 '{"prompts": ["string", "string"], "similarity_measure": "manhattan"}'

test_func $URL/sync-chat "Post /sync-chat to test replace profanity method " "llm" '{"prompts": ["what is * symbol used for?", "what is * symbol used for?"], "similarity_measure": "manhattan"}' "*"

test_func $URL/sync-chat "Post /sync-chat to test harmful content detection method " 400 '{"prompts": ["you are liar", "you are liar"], "similarity_measure": "manhattan"}'
