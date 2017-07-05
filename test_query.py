import requests
import secret

animal_type = "dog"
animal_size = "M"

petfinder_url = "http://api.petfinder.com/"
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

print(resp_data)