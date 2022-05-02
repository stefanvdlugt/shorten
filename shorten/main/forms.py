from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, SubmitField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from ..models import ShortenedURL
import re

class URLForm(FlaskForm):
    dest = StringField('Destination', validators=[DataRequired()])
    custom = RadioField('Shortened URL', default='random', choices=[('random','Random'), ('manual','Custom')])
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
            if ShortenedURL.query.filter_by(slug=field.data).count() > 0:
                raise ValidationError('That shortened URL already exists!')

class DeleteURLForm(FlaskForm):
    slug = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Delete')

    def validate_slug(form, field):
        slug = field.data
        if ShortenedURL.query.filter_by(slug=slug).count() == 0:
            raise ValidationError("This URL does not exist.")

class EditURLForm(FlaskForm):
    dest = StringField('Destination')
    oldslug = HiddenField(validators=[DataRequired()])
    newslug = StringField('Slug')
    submit = SubmitField('Save changes')

    def validate_oldslug(form, field):
        slug = field.data
        if ShortenedURL.query.filter_by(slug=slug).count() == 0:
            raise ValidationError("This URL does not exist.")

    def validate_dest(form, field):
        if not any(field.data.startswith(s) for s in ['http://', 'https://']):
            raise ValidationError("Not a valid HTTP/HTTPS URL.")

    def validate_newslug(form, field):
        if not field.data:
            raise ValidationError(
                'Insert a slug'
            )
        if re.search(r'^[A-Za-z0-9\.\-\_]+$', field.data) is None:
            raise ValidationError((
                'The following characters are allowed:'
                'A-Z, a-z, 0-9, ._-'
            ))
        if form.oldslug.data != form.newslug.data and ShortenedURL.query.filter_by(slug=field.data).count() > 0:
            raise ValidationError('That shortened URL already exists!')


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class MultiSelectURLForm(FlaskForm):
    boxes = MultiCheckboxField('Checked', validate_choice=False)
    submit = SubmitField('Delete selected')
