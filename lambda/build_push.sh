#!/bin/bash

# make staging directory
# perhaps only copy src from docker home
# use create or update depending on if function exists
# set name and role from env or cmd line

cd /home/lambda

pip install -t /home/lambda -r requirements.txt
zip -r9 /tmp/lambda.zip *

# aws lambda create-function \
#   --function-name aata-eta \
#   --runtime python2.7 \
#   --role arn:aws:iam::163470284239:role/service-role/lambda-example-role \
#   --handler lambda_handler.lambda_handler --publish \
#   --zip-file fileb:///tmp/lambda.zip

aws lambda update-function-code \
  --function-name aata-eta \
  --publish \
  --zip-file fileb:///tmp/lambda.zip


# RUN zip -9 /tmp/lambda.zip *
#  update-function-code --function-name <value> [--zip-file <value>] --publish
#

# create-function --function-name aata-eta --runtime python2.7 --role <value>
# --handler eta.handler --publish --zip-file
# [--description <value>]
# [--timeout <value>]
# [--memory-size <value>]

