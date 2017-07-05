# Fluffy Finder - Chatbot
[![GitHub Issues](https://img.shields.io/github/issues/t04glovern/fluffy-finder-chatbot.svg)](https://github.com/t04glovern/fluffy-finder-chatbot/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

Chatbot for the AWS chatbot challenge 2017. It aims to help people find animals that need love using Amazon LEX, Lambda and Slack chat integration

<p align="center"><img width=60 src="https://github.com/t04glovern/fluffy-finder-chatbot/blob/master/images/demo-01.png"></p>

## Install

#### Lambda `get_pet_info`

1. Generate a `petfinder` API key from `https://www.petfinder.com/developers/api-key`
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

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
