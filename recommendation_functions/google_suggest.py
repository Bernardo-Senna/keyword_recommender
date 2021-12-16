import json
import requests

def get_recommendation_suggest(seed_keyword):
    """get the list of auto-complete suggestions of google search"""
    try:
        url = f'http://suggestqueries.google.com/complete/search?client=firefox&q={seed_keyword}'
        headers = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        keywords_result_list = json.loads(response.content.decode('utf-8'))
        keywords_result_list = keywords_result_list[1]

        return keywords_result_list

    except ValueError:
        return "invalid input"