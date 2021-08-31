from flask import Flask
from flask import request
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
    keyword = request.args.get("keyword", "")
    if keyword:
        keyword_recommendation_list = get_recommendation(keyword)
    else:
        keyword_recommendation_list = ""
    return (
        """
            <form action="" method="get">
                <h2>Keyword Recommender</h2>
                <input type="text" name="keyword">
                <input type="submit" value="search">
            </form>
        """
        + "<h4>Recommended keywords for you: </h4>"
        + keyword_recommendation_list
    )


def get_recommendation(input_term):
    """get the list of recommended keyword to use"""
    try:
        # build the payload for given keyword
        pytrends = TrendReq(hl='pt-BR', tz=180)
        pytrends.build_payload(kw_list=[input_term], cat='0', timeframe='now 7-d', geo='BR-MG', gprop='')

        # create initial dataframes of keywords (top and rising recommendations of google trends)
        df_top_list_related_queries = pd.DataFrame(columns=['query', 'value'])
        df_rising_list_related_queries = pd.DataFrame(columns=['query', 'value'])

        related_queries = pytrends.related_queries()

        if related_queries[input_term].get('top') is not None:
            df_top_list_related_queries = related_queries[input_term].get('top')

        if related_queries[input_term].get('rising') is not None:
            df_rising_list_related_queries = related_queries[input_term].get('rising')

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

        # convert the list to string (including html format tags) for response request
        result_string = "<ul>"
        for keyword in keywords_result_list:
            result_string += "<li>" + keyword + "</li>"
        result_string += "</ul>"

        return result_string

    except ValueError:
        return "invalid input"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
