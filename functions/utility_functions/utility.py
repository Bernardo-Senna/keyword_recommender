from flask_table import Table, Col

def get_result_list(result_string):
    keyword_recommendation_list = """<div><ul>"""

    for term in result_string:
        keyword_recommendation_list += f'<li>{term}</li>'

    keyword_recommendation_list += """</ul></div>"""

    return keyword_recommendation_list


def remove_duplicates_from_list(inputted_list: list):
    
    clean_result_string = []
    for term in inputted_list:
        if term not in clean_result_string:
            clean_result_string.append(term)

    return clean_result_string


def remove_extremely_long_terms_from_list(inputted_list: list):

    for term in inputted_list:
        if len(term) > 100:
            inputted_list.remove(term)

    return inputted_list
