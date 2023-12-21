import json
import random
import time
import requests

user_codes_to_generate = input('Enter how many codes to generate (recommended 200 or less):') or '5'
user_delay = input('Enter delay in milliseconds per code:') or '1000'

codes_to_generate = int(user_codes_to_generate) or 5
delay = int(user_delay) or 1000

def generate_promo_code_links():
    saved_uuid = 'systemData'
    discord_base_url = 'https://discord.com/billing/partner-promotions'
    discord_api_url = 'https://api.discord.gx.games/v1/direct-fulfillment'
    promotion_id = '1180231712274387115'

    def generate_uuid():
        return '-'.join([
            f'{random.randint(0, 0xffff):04x}',
            f'{random.randint(0, 0xffff):04x}',
            f'{random.randint(0, 0xffff):04x}',
            f'{random.randint(0, 0xfff) | 0x4000:04x}',
            f'{random.randint(0, 0x3fff) | 0x8000:04x}',
            f'{random.randint(0, 0xffff):04x}',
        ])

    def init_request_to_discord(uuid):
        request_data = {'partnerUserId': uuid}

        try:
            response = requests.post(discord_api_url, headers={'Content-Type': 'application/json'},
                                     data=json.dumps(request_data))

            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as error:
            print('Error:', error)
            raise error

    def generate_and_show_promo_url():
        uuid = generate_uuid()
        response = init_request_to_discord(uuid)
        return f'{discord_base_url}/{promotion_id}/{response["token"]}'

    def generate_multiple_promo_urls():
        promo_links = []
        with open('promo_code_links_py.txt', 'a') as file:
            for _ in range(codes_to_generate):
                link = generate_and_show_promo_url()
                promo_links.append(link)
                file.write(link + '\n')
                time.sleep(delay / 1000)

        return promo_links

    return generate_multiple_promo_urls()

def display_promo_code_links():
    print('Your Links Are Currently Being Generated. Estimated Time:', (codes_to_generate * delay) / 1000, 'Seconds')

    try:
        links = generate_promo_code_links()

        print('DONE! Enjoy the nitro!')
        print('\nGenerated Promo Code Links: ')
        for link in links:
            print(link)
        print('\nAll links saved to promo_code_links_py.txt')

    except Exception as error:
        print('Error generating promo code links:', error)

display_promo_code_links()
