# Fluffy Finder - Chatbot
[![GitHub Issues](https://img.shields.io/github/issues/t04glovern/fluffy-finder-chatbot.svg)](https://github.com/t04glovern/fluffy-finder-chatbot/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

Chatbot for the AWS chatbot challenge 2017.

<p align="center"><img width=60%% src="https://github.com/t04glovern/fluffy-finder-chatbot/blob/master/images/demo-01.png"></p>

It aims to help people find animals that need love using Amazon LEX, Lambda and Slack chat integration.

## Install

### Lambda `get_pet_info`

1. Generate a `petfinder` API key from `https://www.petfinder.com/developers/api-key` (or use my one in secret.py)
2. Create a `secret.py` file to replace the `secret-example.py` file in the `lambda/` directory
3. From the root directory of this repo run `build-lambda.sh` to build the zip file including pip dependencies.
4. Upload this zip (placed in the `builds` folder of the root directory) to the lambda dashboard.
5. Use the following settings when defining the lambda function:

```
Runtime:        Python 3.6
Handler:        get_pet_info.lambda_handler
Role:           Choose an existing role (this bit is up to you though)
Existing Role:  lambda_basic_execution
Description:    Functions used to get pet info
```

You can run `aws lambda update-function-code --function-name "get_pet_info" --zip-file fileb://builds/lambda-build.zip` from the root directory to update the code

### Lex Bot Overview

#### Bot

> **Name:** FluffyFinder

#### Intents

> **Name:** GetHelpWithPets

> **Name:** GetMyPetMatch

> **Name:** GetPetInfo

> **Name:** ListPets

### Exporting bot-definition

1. Change the `ACTIVATE_PATH=` line to a python2.7 interpreter or virtualenv
2. Run the `export-chatbot.sh` script to generate the `bot-definition-export.json` file in the `lex/` directory
