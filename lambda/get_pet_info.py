import boto3
import requests
import secret


animals = [
    'barnyard',
    'bird',
    'cat',
    'dog',
    'horse',
    'reptile',
    'smallfurry'
]

petfinder_url = "http://api.petfinder.com/"


def build_response(message):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    }


def lambda_handler(event, context):
    if 'ListPets' == event['currentIntent']['name']:
        options = animals
        msg = ""
        for i, option in enumerate(options):
            msg += "{} - {}\n".format(i, option)
        return build_response(msg)

    elif 'GetMyPetMatch' == event['currentIntent']['name']:
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

        r = requests.post((petfinder_url + petfinder_query), params=petfinder_payload)
        resp_data = r.json()

        text = ""
        animal_name = resp_data['petfinder']['pet']['name']['$t']
        animal_type = resp_data['petfinder']['pet']['animal']['$t']
        animal_description = resp_data['petfinder']['pet']['description']['$t']
        animal_photos = resp_data['petfinder']['pet']['media']['photos']['photo'][3]['$t']
        text += "*Name:* {}\n*Type:* {}\n*Photo:* {}\n\n*Description:* {}".format(animal_name, animal_type, animal_photos, animal_description)

        return build_response(text)

    elif 'GetPetInfo' == event['currentIntent']['name']:
        animal_type = event['currentIntent']['slots']['animal_type']

        petfinder_query = "breed.list"
        petfinder_payload = {
            'key': secret.PETFINDER_API_KEY,
            'format': 'json',
            'animal': animal_type
        }

        r = requests.post((petfinder_url + petfinder_query), params=petfinder_payload)
        resp_data = r.json()

        msg = ""
        for breed in resp_data['petfinder']['breeds']['breed']:
            msg += "{}\n".format(breed)
        return build_response(msg)
