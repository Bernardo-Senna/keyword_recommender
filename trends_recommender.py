from pytrends.request import TrendReq
import pandas as pd
import sys


def main():
    args = sys.argv[1:]

    # build the payload for given keyword
    pytrends = TrendReq(hl='pt-BR', tz=180)
    pytrends.build_payload(kw_list=[args[0]], cat='0', timeframe='now 7-d', geo='BR-MG', gprop='')

    # create initial dataframes of keywords (top and rising recommendations of google trends)
    df_top_list_related_queries = pd.DataFrame(columns=['query', 'value'])
    df_rising_list_related_queries = pd.DataFrame(columns=['query', 'value'])

    related_queries = pytrends.related_queries()

    if related_queries[args[0]].get('top') is not None:
        df_top_list_related_queries = related_queries[args[0]].get('top')

    if related_queries[args[0]].get('rising') is not None:
        df_rising_list_related_queries = related_queries[args[0]].get('rising')

    # build list of related keywords to increase recommendation range of terms
    list_related_queries = []
    list_related_queries += list(df_top_list_related_queries['query']) + list(df_rising_list_related_queries['query'])

    for keyword in list_related_queries:
        # build the payload and get related queries for each keyword in list_related_queries
        pytrends.build_payload(kw_list=[keyword], cat='0', timeframe='now 7-d', geo='BR-MG', gprop='')
        related_queries = pytrends.related_queries()
        if related_queries[keyword].get('top') is not None:
            df_top_list_related_queries = \
                pd.concat([df_top_list_related_queries, related_queries[keyword].get('top')], ignore_index=True)

        if related_queries[keyword].get('rising') is not None:
            df_rising_list_related_queries = \
                pd.concat([df_rising_list_related_queries, related_queries[keyword].get('rising')], ignore_index=True)

    # return the final list of recommended keywords by google trends
    df_result_trends = pd.concat([df_top_list_related_queries, df_rising_list_related_queries], ignore_index=True)
    keywords_result_list = list(df_result_trends['query'][df_result_trends['value'] >= 50])
    print(keywords_result_list)


if __name__ == '__main__':
    main()
