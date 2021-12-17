from flask import Flask, flash, render_template, request, redirect
from functions.recommendation_functions import google_trends, google_suggest
from functions.utility_functions import utility
from forms import SearchForm

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    index_form = SearchForm(request.form)
    result_string = []
    error_flag = 0

    if request.method == 'POST':
        search_string = index_form.user_text.data
        if search_string:
            result_string = google_trends.get_recommendation_trends(
                search_string) + google_suggest.get_recommendation_suggest(search_string)
            result_string = utility.remove_duplicates_from_list(result_string)
            result_string = utility.remove_extremely_long_terms_from_list(
                result_string)

            # clean user inputted text
            index_form.user_text.data = ""

            # display results
            return render_template('index.html', form=[index_form, result_string, error_flag])
        else:
            error_flag = 1
            error_message = "No recommended keywords for you or invalid text inserted in search field :("
            return render_template('index.html', form=[index_form, error_message, error_flag])

    return render_template('index.html', form=[index_form, result_string, error_flag])


if __name__ == '__main__':
    app.run()
