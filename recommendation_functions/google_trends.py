import json
import pandas as pd
from pytrends.request import TrendReq

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