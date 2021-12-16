from wtforms import Form, StringField, SelectField


class SearchForm(Form):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search recommend words:', choices=choices)
    search = StringField('')
