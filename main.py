from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location', validators=[DataRequired(), URL()])
    open = StringField('Open', validators=[DataRequired()])
    close = StringField('Close', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', validators=[DataRequired()], choices=['✘','☕','☕☕','☕☕☕','☕☕☕☕'])
    wifi = SelectField('WiFi Rating', validators=[DataRequired()], choices=['✘','💪', '💪💪', '💪💪💪','💪💪💪💪'])
    power_rating = SelectField("Power Socket Availability", validators=[DataRequired()], choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=('GET', 'POST'))
def add_cafe():
    new_list = []
    form = CafeForm()
    if form.validate_on_submit():
        new_list.append(form.cafe.data)
        new_list.append(form.location.data)
        new_list.append(form.open.data)
        new_list.append(form.close.data)
        new_list.append(form.coffee.data)
        new_list.append(form.wifi.data)
        new_list.append(form.power_rating.data)
        with open('cafe-data.csv', 'a', newline='\n', encoding='utf-8') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(new_list)

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
