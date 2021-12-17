from flask import Flask, flash, render_template, request, redirect
from functions.recommendation_functions import google_trends, google_suggest
from functions.utility_functions import utility
from forms import SearchForm

# _DEFAULT_LOCATION_IDS = ["2076"]  # location ID for Brazil

# _DEFAULT_LANGUAGE_ID = "1014"  # language ID for Portuguese

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    search_string = SearchForm(request.form)
    if search_string:
        if request.method == 'POST':
            return search_results(search_string)
        return render_template('index.html', form=search_string)


@app.route('/results')
def search_results(search_string):

    result_string = google_trends.get_recommendation_trends(search_string) + google_suggest.get_recommendation_suggest(search_string)
    result_string = utility.remove_duplicates_from_list(result_string)
    result_string = utility.remove_extremely_long_terms_from_list(result_string)

    if not result_string:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        result_string = utility.get_result_list(result_string)
        return render_template('results.html', results=result_string)


if __name__ == '__main__':
    app.run()


# @app.route("/")
# def index():

#     keyword = request.args.get("keyword", "")

#     

#         # convert the list to string (including html format tags) for response request
#         keyword_recommendation_list = """
#                                         <div class="response-title">
#                                             <h4 align="center">Recommended keywords for you: </h4>
#                                         </div>
#                                         <div class="keyword-list">
#                                             <ul>
#                                       """

#         for term in result_string:
#             keyword_recommendation_list += f'<li>{term}</li>'

#         keyword_recommendation_list += """
#                                                 </ul>
#                                             </div>
#                                         </body>
#                                        """
#     else:
#         keyword_recommendation_list = ""

#     return (
#         """
#             <style type="text/css">
#                 .wrapper {
#                     margin-top: 100px;
#                     display: flex;
#                     flex-direction: row;
#                     justify-content: center;
#                 }

#                 .response-title{
#                     display: flex;
#                     flex-direction: row;
#                     justify-content: center;
#                     align-items: center;
#                     margin-right: 110px;
#                 }

#                 .keyword-list {
#                     display: flex;
#                     flex-direction: row;
#                     justify-content: center;
#                     align-items: center;
#                     margin-left: 40%;
#                     margin-right: 42%;
#                 }

#                 #index-title {
#                     color: #2477ad;
#                 }
#             </style>

#             <head>
#                 <link rel="icon" type="image/png" href="favicon.png"/>
#             </head>
#             <body>
#                 <div class="wrapper">
#                     <form id="index-page" action="" method="get">
#                         <h1 id="index-title">Keyword Recommender</h1>
#                         <input type="text" name="keyword" size="35">
#                         <input type="submit" value="search">
#                     </form>
#                 </div>
#         """
#         + keyword_recommendation_list
#     )
