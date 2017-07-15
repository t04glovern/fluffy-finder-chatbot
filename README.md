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

### Lex Bot Overview

#### Bot

**Name:** FluffyFinder

#### Intents

**Name:** GetMyPetMatch

<p align="center"><img width=80%% src="https://github.com/t04glovern/fluffy-finder-chatbot/blob/master/images/bot-image-01.png"></p>

**Name:** GetPetInfo

<p align="center"><img width=80%% src="https://github.com/t04glovern/fluffy-finder-chatbot/blob/master/images/bot-image-02.png"></p>

**Name:** ListPets

<p align="center"><img width=80%% src="https://github.com/t04glovern/fluffy-finder-chatbot/blob/master/images/bot-image-03.png"></p>

### Exporting bot-definition

1. Change the `ACTIVATE_PATH=` line to a python2.7 interpreter or virtualenv
2. Run the `export-chatbot.sh` script to generate the `bot-definition-export.json` file in the `lex/` directory

#### Bot Definition

```yaml
{
  "bot": {
    "abortStatement": {
      "messages": [
        {
          "content": "Sorry, I could not understand. Goodbye.", 
          "contentType": "PlainText"
        }
      ]
    }, 
    "childDirected": false, 
    "clarificationPrompt": {
      "maxAttempts": 5, 
      "messages": [
        {
          "content": "Sorry, can you please repeat that?", 
          "contentType": "PlainText"
        }
      ]
    }, 
    "idleSessionTTLInSeconds": 60, 
    "intents": [
      {
        "intentName": "ListPets", 
        "intentVersion": "$LATEST"
      }, 
      {
        "intentName": "GetPetInfo", 
        "intentVersion": "$LATEST"
      }, 
      {
        "intentName": "GetMyPetMatch", 
        "intentVersion": "$LATEST"
      }
    ], 
    "locale": "en-US", 
    "name": "FluffyFinder", 
    "voiceId": "Ivy"
  }, 
  "intents": [
    {
      "confirmationPrompt": {
        "maxAttempts": 3, 
        "messages": [
          {
            "content": "We're going to search for a {pet_sizes} pet that makes a {pet_sounds} sound. Is this correct?", 
            "contentType": "PlainText"
          }
        ]
      }, 
      "fulfillmentActivity": {
        "codeHook": {
          "messageVersion": "1.0", 
          "uri": "arn:aws:lambda:us-east-1:277790246569:function:get_pet_info"
        }, 
        "type": "CodeHook"
      }, 
      "name": "GetMyPetMatch", 
      "rejectionStatement": {
        "messages": [
          {
            "content": "No problem, maybe we'll search for you another time!", 
            "contentType": "PlainText"
          }
        ]
      }, 
      "sampleUtterances": [
        "Find my perfect match", 
        "Find me perfect pet", 
        "Guess my perfect match", 
        "Guess my pet"
      ], 
      "slots": [
        {
          "name": "pet_sounds", 
          "priority": 2, 
          "sampleUtterances": [], 
          "slotConstraint": "Required", 
          "slotType": "pet_sounds", 
          "slotTypeVersion": "$LATEST", 
          "valueElicitationPrompt": {
            "maxAttempts": 2, 
            "messages": [
              {
                "content": "What sound does you dream pet make?", 
                "contentType": "PlainText"
              }
            ], 
            "responseCard": "{\"version\":1,\"contentType\":\"application/vnd.amazonaws.card.generic\",\"genericAttachments\":[{\"imageUrl\":\"http://i.imgur.com/oKnwkgA.png\",\"subTitle\":\"What sound does your new friend make?\",\"title\":\"Pet Sound\",\"buttons\":[{\"text\":\"Woof\",\"value\":\"Woof\"},{\"text\":\"Meow\",\"value\":\"Meow\"},{\"text\":\"Chirp\",\"value\":\"Chirp\"},{\"text\":\"Hiss\",\"value\":\"Hiss\"}]}]}"
          }
        }, 
        {
          "name": "pet_sizes", 
          "priority": 1, 
          "sampleUtterances": [], 
          "slotConstraint": "Required", 
          "slotType": "pet_sizes", 
          "slotTypeVersion": "$LATEST", 
          "valueElicitationPrompt": {
            "maxAttempts": 2, 
            "messages": [
              {
                "content": "What size is your dream pet?", 
                "contentType": "PlainText"
              }
            ], 
            "responseCard": "{\"version\":1,\"contentType\":\"application/vnd.amazonaws.card.generic\",\"genericAttachments\":[{\"imageUrl\":\"http://i.imgur.com/d5CqkQB.png\",\"subTitle\":\"Do you want a small and agile or a tubby but cuddly friend?\",\"title\":\"Pet Size\",\"buttons\":[{\"text\":\"Small\",\"value\":\"Small\"},{\"text\":\"Medium\",\"value\":\"Medium\"},{\"text\":\"Large\",\"value\":\"Large\"},{\"text\":\"Extra-Large\",\"value\":\"Extra-Large\"}]}]}"
          }
        }
      ]
    }, 
    {
      "fulfillmentActivity": {
        "codeHook": {
          "messageVersion": "1.0", 
          "uri": "arn:aws:lambda:us-east-1:277790246569:function:get_pet_info"
        }, 
        "type": "CodeHook"
      }, 
      "name": "ListPets", 
      "sampleUtterances": [
        "What pets are available", 
        "What is up for adoption", 
        "What's available"
      ], 
      "slots": []
    }, 
    {
      "fulfillmentActivity": {
        "codeHook": {
          "messageVersion": "1.0", 
          "uri": "arn:aws:lambda:us-east-1:277790246569:function:get_pet_info"
        }, 
        "type": "CodeHook"
      }, 
      "name": "GetPetInfo", 
      "sampleUtterances": [
        "Find me {animal_type}", 
        "I'm looking for {animal_type}", 
        "I want a {animal_type}"
      ], 
      "slots": [
        {
          "name": "animal_type", 
          "priority": 1, 
          "sampleUtterances": [], 
          "slotConstraint": "Required", 
          "slotType": "AMAZON.Animal", 
          "valueElicitationPrompt": {
            "maxAttempts": 2, 
            "messages": [
              {
                "content": "Which animal type?", 
                "contentType": "PlainText"
              }
            ]
          }
        }
      ]
    }
  ], 
  "slot_types": [
    {
      "description": "Pet sound types", 
      "enumerationValues": [
        {
          "value": "Chirp"
        }, 
        {
          "value": "Hiss"
        }, 
        {
          "value": "Meow"
        }, 
        {
          "value": "Woof"
        }
      ], 
      "name": "pet_sounds"
    }, 
    {
      "description": "Pet Size types", 
      "enumerationValues": [
        {
          "value": "Extra-Large"
        }, 
        {
          "value": "Small"
        }, 
        {
          "value": "Medium"
        }, 
        {
          "value": "Large"
        }
      ], 
      "name": "pet_sizes"
    }
  ]
}
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
