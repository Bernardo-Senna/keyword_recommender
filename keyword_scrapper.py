from pytrends.request import TrendReq
import pandas as pd
import time
import sys
import os


def main():
    args = sys.argv[1:]

    # The directory that you want to save the CSV to
    if not os.path.exists('./data'):
        os.mkdir('./data')

    data_path = './data'

    # build the payload for given keyword
    pytrends = TrendReq(hl='pt-BR', tz=180)
    pytrends.build_payload(kw_list=[args[0]], cat='0', timeframe='now 7-d', geo='BR-MG', gprop='')

    initial_keyword_recommendation_list = []

    related_queries = pytrends.related_queries()
    top_list_related_queries = related_queries[args[0]].get('top')
    if top_list_related_queries is not None:
        top_list_related_queries = list(top_list_related_queries.get('query'))
        initial_keyword_recommendation_list += top_list_related_queries

    rising_list_related_queries = related_queries[args[0]].get('rising')
    if rising_list_related_queries is not None:
        rising_list_related_queries = list(rising_list_related_queries.get('query'))
        initial_keyword_recommendation_list += rising_list_related_queries

    # print("=========================================================================================================")
    # test3 = pytrends.related_topics()
    # df_test3 = pd.DataFrame.from_dict(test3, orient='index')
    # print(df_test3)
    final_keyword_recommendation_list = []

    for item in initial_keyword_recommendation_list:

        pytrends.build_payload(kw_list=[item], cat='0', timeframe='now 7-d', geo='BR-MG', gprop='')
        related_queries = pytrends.related_queries()

        top_list_related_queries = related_queries[item].get('top')
        if top_list_related_queries is not None:
            top_list_related_queries = list(top_list_related_queries.get('query'))
            final_keyword_recommendation_list += top_list_related_queries

        rising_list_related_queries = related_queries[item].get('rising')
        if rising_list_related_queries is not None:
            rising_list_related_queries = list(rising_list_related_queries.get('query'))
            final_keyword_recommendation_list += rising_list_related_queries

    print(final_keyword_recommendation_list)


if __name__ == '__main__':
    main()
