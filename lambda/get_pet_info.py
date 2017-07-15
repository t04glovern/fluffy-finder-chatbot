import boto3
import requests
import logging

# Local secret and configuration settings
import secret
import config

# Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class LexEvent:
    def __init__(self, event):
        self.event = event
        self.slots = event['currentIntent']['slots']
        self.intent = event['currentIntent']['name']
        self.input_text = event['inputTranscript']
        self.sess_attr = event['sessionAttributes']
        self.invocation = event['invocationSource']

    def build_response(self, message):
        return {
            'sessionAttributes': self.sess_attr,
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": message
                }
            }
        }


def list_pets(lex):
    options = config.petfinder_animal_types
    msg = ""
    for i, option in enumerate(options):
        msg += "{} - {}\n".format(i, option)
    return lex.build_response(msg)


def my_perfect_match(lex):
    pet_size = lex.slots['pet_sizes']
    pet_sound = lex.slots['pet_sounds']

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
    animal_name = resp_data['petfinder']['pet']['name']['$t']
    animal_type = resp_data['petfinder']['pet']['animal']['$t']
    animal_description = resp_data['petfinder']['pet']['description']['$t']
    animal_photos = resp_data['petfinder']['pet']['media']['photos']['photo'][3]['$t']
    text += "*Name:* {}\n*Type:* {}\n*Photo:* {}\n\n*Description:* {}".format(animal_name, animal_type, animal_photos,
                                                                              animal_description)

    return lex.build_response(text)


def pet_info(lex):
    animal_type = lex.slots['animal_type']

    petfinder_query = "breed.list"
    petfinder_payload = {
        'key': secret.PETFINDER_API_KEY,
        'format': 'json',
        'animal': animal_type
    }

    r = requests.post((config.petfinder_url + petfinder_query), params=petfinder_payload)
    resp_data = r.json()

    msg = ""
    for breed in resp_data['petfinder']['breeds']['breed']:
        msg += "{}\n".format(breed)
    return lex.build_response(msg)


def get_help(lex):
    option_selected = lex.slots['fluffy_option']

    if option_selected == "list_pet_types":
        return lex.build_response("type: What pets are available?")
    if option_selected == "find_me_random":
        return lex.build_response("type: Find my perfect pet?")
    if option_selected == "how_can_i_help":
        return lex.build_response("Fostering animals is a great way to help without making long term commitments!")
    else:
        return not_understood(lex)


def not_understood(lex):
    return lex.fulfill("You're going to have to be more clear sorry.")


def fluffy_functions(lex):

    if lex.intent == "ListPets":
        return list_pets(lex)
    if lex.intent == "GetMyPetMatch":
        return my_perfect_match(lex)
    if lex.intent == "GetPetInfo":
        return pet_info(lex)
    if lex.intent == "GetHelpWithPets":
        return get_help(lex)
    else:
        return not_understood(lex)


def lambda_handler(event, context=None):
    lex = LexEvent(event)
    logger.info(('IN', event))

    try:
        res = fluffy_functions(lex)
        logger.info(('OUT', res))
        return res
    except Exception as e:
        logger.error(e)


