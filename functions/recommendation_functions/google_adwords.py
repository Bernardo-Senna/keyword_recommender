

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