from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, SubmitField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from ..models import ShortenedURL
import re

class URLForm(FlaskForm):
    dest = StringField('Destination', validators=[DataRequired()])
    custom = RadioField('URL type', default='random', choices=[('random','Random'), ('manual','Custom')])
    customurl = StringField('Custom slug')
    submit = SubmitField('Submit')

    def validate_dest(form, field):
        if not any(field.data.startswith(s) for s in ['http://', 'https://']):
            raise ValidationError("Not a valid HTTP/HTTPS URL.")

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

class DeleteURLForm(FlaskForm):
    slug = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Delete')

    def validate_slug(form, field):
        slug = field.data
        if ShortenedURL.query.filter_by(slug=slug).count() == 0:
            raise ValidationError("This URL does not exist.")
