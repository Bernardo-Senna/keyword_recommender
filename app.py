import json
import pandas as pd
import requests
from flask import Flask
from flask import request
from pytrends.request import TrendReq

# _DEFAULT_LOCATION_IDS = ["2076"]  # location ID for Brazil

# _DEFAULT_LANGUAGE_ID = "1014"  # language ID for Portuguese

app = Flask(__name__)


@app.route("/")
def index():
    keyword = request.args.get("keyword", "")
    if keyword:
        result_string = get_recommendation_trends(keyword) + get_recommendation_suggest(keyword)

        # remove duplicates from result
        clean_result_string = []
        for term in result_string:
            if term not in clean_result_string:
                clean_result_string.append(term)

        # convert the list to string (including html format tags) for response request
        keyword_recommendation_list = """
                                        <div class="response-title">
                                            <h4 align="center">Recommended keywords for you: </h4>
                                        </div>
                                        <div class="keyword-list">
                                            <ul>
                                      """

        for term in clean_result_string:
            keyword_recommendation_list += f'<li>{term}</li>'

        keyword_recommendation_list += """
                                                </ul>
                                            </div>
                                        </body>
                                       """
    else:
        keyword_recommendation_list = ""

    return (
        """
            <style type="text/css">
                .wrapper {
                    margin-top: 100px;
                    display: flex;
                    flex-direction: row;
                    justify-content: center;
                    align-items: center;
                }
                
                .response-title{
                    display: flex;
                    flex-direction: row;
                    justify-content: center;
                    align-items: center;
                    margin-right: 110px;
                }
                
                .keyword-list {
                    display: flex;
                    flex-direction: row;
                    justify-content: center;
                    align-items: center;
                }
                
                #index-title {
                    color: #2477ad;
                }
            </style>
            
            <head>
                <link rel="icon" type="image/png" href="favicon.png"/>
            </head>
            <body>
                <div class="wrapper">
                    <form id="index-page" action="" method="get">
                        <h1 id="index-title">Keyword Recommender</h1>
                        <input type="text" name="keyword" size="35">
                        <input type="submit" value="search">
                    </form>
                </div>
        """
        + keyword_recommendation_list
    )


def get_recommendation_trends(seed_keyword):
    """get the list of recommended keyword to use (from Google Trends)"""
    try:
        # build the payload for given keyword
        pytrends = TrendReq(hl='pt-BR', tz=180)
        pytrends.build_payload(kw_list=[seed_keyword], cat='0', timeframe='now 7-d', geo='BR', gprop='')

        # create initial dataframes of keywords (top and rising recommendations of google trends)
        df_top_list_related_queries = pd.DataFrame(columns=['query', 'value'])
        df_rising_list_related_queries = pd.DataFrame(columns=['query', 'value'])

        related_queries = pytrends.related_queries()

        if related_queries[seed_keyword].get('top') is not None:
            df_top_list_related_queries = related_queries[seed_keyword].get('top')

        if related_queries[seed_keyword].get('rising') is not None:
            df_rising_list_related_queries = related_queries[seed_keyword].get('rising')

        if (related_queries[seed_keyword].get('top') is not None) or (related_queries[seed_keyword].get('rising') is not None):
            if (related_queries[seed_keyword].get('top').shape[0] + related_queries[seed_keyword].get('top').shape[0]) < 10:
                # build list of related keywords to increase recommendation range of terms
                list_related_queries = []
                list_related_queries += list(df_top_list_related_queries['query']) + list(df_rising_list_related_queries['query'])

                for keyword in list_related_queries:
                    # build the payload and get related queries for each keyword in list_related_queries
                    pytrends.build_payload(kw_list=[keyword], cat='0', timeframe='now 7-d', geo='BR', gprop='')
                    related_queries = pytrends.related_queries()
                    if related_queries[keyword].get('top') is not None:
                        df_top_list_related_queries = \
                            pd.concat([df_top_list_related_queries,
                                       related_queries[keyword].get('top').sort_values(by='value', ascending=False).head(2)],
                                      ignore_index=True)

                    if related_queries[keyword].get('rising') is not None:
                        df_rising_list_related_queries = \
                            pd.concat([df_rising_list_related_queries,
                                       related_queries[keyword].get('rising').sort_values(by='value', ascending=False).head(2)],
                                      ignore_index=True)

        # return the final list of recommended keywords by google trends
        df_result_trends = pd.concat([df_top_list_related_queries, df_rising_list_related_queries], ignore_index=True)
        keywords_result_list = list(df_result_trends['query'])

        return keywords_result_list

    except ValueError:
        return "invalid input"


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


# def _map_locations_ids_to_resource_names(client, location_ids):
#     """Converts a list of location IDs to resource names.
#     Args:
#         client: an initialized GoogleAdsClient instance.
#         location_ids: a list of location ID strings.
#     Returns:
#         a list of resource name strings using the given location IDs.
#     """
#     build_resource_name = client.get_service("GeoTargetConstantService").geo_target_constant_path
#     return [build_resource_name(location_id) for location_id in location_ids]
#
#
# def get_recommendation_planner(seed_keyword):
#     """get the list of recommended keyword to use (from Google Keyword Planner)"""
#     try:
#         googleads_client = GoogleAdsClient.load_from_storage("google-ads.yaml")
#
#         client = googleads_client
#         customer_id = "7810420786"
#         location_ids = str(_DEFAULT_LOCATION_IDS)
#         language_id = str(_DEFAULT_LANGUAGE_ID)
#         keyword_texts = str([seed_keyword])
#
#         keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
#         keyword_competition_level_enum = client.get_type(
#             "KeywordPlanCompetitionLevelEnum"
#         ).KeywordPlanCompetitionLevel
#         keyword_plan_network = client.get_type(
#             "KeywordPlanNetworkEnum"
#         ).KeywordPlanNetwork.GOOGLE_SEARCH_AND_PARTNERS
#         location_rns = _map_locations_ids_to_resource_names(client, location_ids)
#         language_rn = client.get_service(
#             "LanguageConstantService"
#         ).language_constant_path(language_id)
#
#         keyword_annotation = client.enums.KeywordPlanKeywordAnnotationEnum
#
#         # Keyword are required to generate keyword ideas
#         if not keyword_texts:
#             raise ValueError("At least one keyword is required")
#
#         request = client.get_type("GenerateKeywordIdeasRequest")
#         request.customer_id = customer_id
#         request.language = language_rn
#         request.geo_target_constants = location_rns
#         request.include_adult_keywords = False
#         request.keyword_plan_network = keyword_plan_network
#         request.keyword_annotation = keyword_annotation
#
#         request.keyword_seed.keywords.extend(keyword_texts)
#
#         keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
#             request=request
#         )
#
#         df_planner_result = pd.DataFrame(columns=['query', 'value'])
#
#         for idea in keyword_ideas:
#             competition_value = idea.keyword_idea_metrics.competition.name
#             length_of_df = len(df_planner_result)
#             df_planner_result.loc[length_of_df] = [idea.text, competition_value]
#
#         df_planner_result.sort_values(by='value', ascending=False)
#
#         keywords_result_list = list(df_planner_result['query'].head(20))
#
#         # convert the list to string (including html format tags) for response request
#         result_string = """
#                             <div class="response-title">
#                                 <h4 align="center">Recommended keywords for you: </h4>
#                             </div>
#                             <div class="keyword-list">
#                                 <ul>
#                         """
#
#         for keyword in keywords_result_list:
#             result_string += f'<li>{keyword}</li>'
#
#         result_string += """
#                                 </ul>
#                             </div>
#                          """
#
#         return result_string
#
#     except ValueError:
#         return "invalid input"


if __name__ == "__main__":
    app.run()
