from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import re

class URLForm(FlaskForm):
    dest = StringField('Destination', validators=[DataRequired()])
    custom = RadioField('URL type', default='random', choices=[('random','Random'), ('manual','Custom')])
    customurl = StringField('Custom slug')
    submit = SubmitField('Submit')


    def validate_customurl(form, field):
        if form.custom.data == 'manual':
            if not field.data:
                raise ValidationError(
                    'Insert a custom slug or choose to '
                    'generate a random one'
                )
            if re.search(r'^[A-Za-z0-9\.\-\_]+$', field.data) is None:
                raise ValidationError((
                    'The following characters are allowed:'
                    'A-Z, a-z, 0-9, ._-'
                ))

