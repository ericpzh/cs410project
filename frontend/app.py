from flask import render_template
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired

class InputForm(FlaskForm):
    field = StringField('*separate by "," no space: ', validators=[DataRequired()])
    submit = SubmitField('Submit')
    def validate_field(self, field):
        if False: ##todo parse it
            raise ValidationError('Must enter more than 1 libraries.')
        else:
            input_libs = field.split(",")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

@app.route('/', methods=['GET', 'POST'])
def index():
    with open("../scraper/data.txt") as file:
        lib_list = [line[1:-2].split(",") for line in file.readlines()]

    form = InputForm()
    if form.validate_on_submit():
        list = [
            {
                'name': 'react-bootstrap',
            },
            {
                'name': 'reactstrap',
            }
        ]
        return render_template('index.html', title='APP', list=list, form=form)
    list = [
        {
            'name': lib_list[0]
        }
    ]
    return render_template('index.html', title='APP', list=list, form=form)


if __name__ == '__main__':
    app.run()
