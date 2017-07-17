import boto3
import requests
import logging

# Local secret and configuration settings
import secret
import config

# Logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def build_response(msg):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": msg
            }
        }
    }


def list_pets():
    options = config.petfinder_animal_types
    msg = ""
    msg += "_Hint: I want a `cat`_\n\n*Pet Types*:\n"
    for i, option in enumerate(options):
        msg += "{}\n".format(option)
    return build_response(msg)


def my_perfect_match(event):
    pet_size = event['currentIntent']['slots']['pet_sizes']
    pet_sound = event['currentIntent']['slots']['pet_sounds']

    animal_type = None
    animal_size = None

    if pet_sound == "Woof":
        animal_type = "dog"
    elif pet_sound == "Meow":
        animal_type = "cat"
    elif pet_sound == "Chirp":
        animal_type = "bird"
    elif pet_sound == "Hiss":
        animal_type = "reptile"

    if pet_size == "Small":
        animal_size = "S"
    elif pet_size == "Medium":
        animal_size = "M"
    elif pet_size == "Large":
        animal_size = "L"
    elif pet_size == "Extra-Large":
        animal_size = "XL"

    petfinder_query = "pet.getRandom"
    petfinder_payload = {
        'key': secret.PETFINDER_API_KEY,
        'format': 'json',
        'output': 'basic',
        'animal': animal_type,
        'size': animal_size
    }

    r = requests.post((config.petfinder_url + petfinder_query), params=petfinder_payload)
    resp_data = r.json()

    text = ""
    msg = generate_output(text, resp_data)

    return build_response(msg)


def get_pet_breed(animal_type, animal_breed):
    text = "Sure!, let's find you a `" + animal_breed + " " + animal_type + "`\n\n"

    petfinder_query = "pet.getRandom"
    petfinder_payload = {
        'key': secret.PETFINDER_API_KEY,
        'format': 'json',
        'output': 'basic',
        'animal': animal_type,
        'breed': animal_breed
    }

    r = requests.post((config.petfinder_url + petfinder_query), params=petfinder_payload)
    resp_data = r.json()

    msg = generate_output(text, resp_data)

    return build_response(msg)


def pet_info(event):
    animal_type = event['currentIntent']['slots']['animal_type']

    petfinder_query = "breed.list"
    petfinder_payload = {
        'key': secret.PETFINDER_API_KEY,
        'format': 'json',
        'animal': animal_type
    }

    r = requests.post((config.petfinder_url + petfinder_query), params=petfinder_payload)
    resp_data = r.json()

    if event['currentIntent']['slots']['animal_breed']:
        for breed in resp_data['petfinder']['breeds']['breed']:
            if event['currentIntent']['slots']['animal_breed'] == breed['$t']:
                return get_pet_breed(animal_type, event['currentIntent']['slots']['animal_breed'])
    else:
        msg = "Here is a list of `" + animal_type + "` breeds!\n\n" + "*Hint*: _I want a " + \
              resp_data['petfinder']['breeds']['breed'][0]['$t'] + " breed of " + animal_type + "_\n\n"
        for breed in resp_data['petfinder']['breeds']['breed']:
            msg += "`{}`, ".format(breed['$t'])
        return build_response(msg)


def get_help(event):
    option_selected = event['currentIntent']['slots']['fluffy_option']

    if option_selected == "list_pet_types":
        return build_response("*Type*: _What pets are available?_")
    if option_selected == "find_me_random":
        return build_response("*Type*: _Find my perfect pet_")
    if option_selected == "how_can_i_help":
        return build_response("*Yay!*\nFostering animals is a great way to help without making long term commitments!\n\n*Cat Haven*: https://www.cathaven.com.au/services/")
    else:
        return not_understood(event)


def not_understood(event):
    return build_response("You're going to have to be more clear sorry.")


def generate_output(init_text, resp_data):
    text = init_text

    animal_name = resp_data['petfinder']['pet']['name']['$t']
    animal_type = resp_data['petfinder']['pet']['animal']['$t']
    animal_options = ""
    if resp_data['petfinder']['pet']['options']['option']:
        if isinstance(resp_data['petfinder']['pet']['options']['option'], list):
            for option in resp_data['petfinder']['pet']['options']['option']:
                animal_options += (config.petfinder_animal_options[option['$t']] + "\n")
        else:
            animal_options += (config.petfinder_animal_options[resp_data['petfinder']['pet']['options']['option']['$t']] + "\n")
    else:
        animal_options = "N/A"
    animal_description = resp_data['petfinder']['pet']['description']['$t']
    animal_photos = ""
    if resp_data['petfinder']['pet']['media']:
        animal_photos = resp_data['petfinder']['pet']['media']['photos']['photo'][3]['$t']
    else:
        animal_photos = "No Photos Attached"
    text += "*Name:* {}\n*Type:* {}\n*Photo:* {}\n*Key Info:* \n{}\n\n*Description:* \n{}".format(animal_name, animal_type, animal_photos, animal_options, animal_description)

    return text



def fluffy_functions(event):
    if event['currentIntent']['name'] == "ListPets":
        return list_pets()
    if event['currentIntent']['name'] == "GetMyPetMatch":
        return my_perfect_match(event)
    if event['currentIntent']['name'] == "GetPetInfo":
        return pet_info(event)
    if event['currentIntent']['name'] == "GetHelpWithPets":
        return get_help(event)
    else:
        return not_understood(event)


def lambda_handler(event, context=None):
    logger.info(('IN', event))

    '''
    slots = event['currentIntent']['slots']
    intent = event['currentIntent']['name']
    input_text = event['inputTranscript']
    sess_attr = event['sessionAttributes']
    invocation = event['invocationSource']
    '''

    try:
        res = fluffy_functions(event)
        logger.info(('OUT', res))
        return res
    except Exception as e:
        logger.error(e)
