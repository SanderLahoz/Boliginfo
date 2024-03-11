from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Optional, InputRequired, NumberRange


class RequiredIf(DataRequired):
    """Validator which makes a field required if another field is set and has a truthy value.
       Source https://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms"""

    field_flags = ('requiredif',)

    def __init__(self, other_field_name, message=None, *args, **kwargs):
        self.other_field_name = other_field_name
        self.message = message

    def __call__(self, form, field):
        other_field = form[self.other_field_name]
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class PostnummerForm(FlaskForm):
    region_id = StringField('Region_id', validators=[DataRequired()])
    submit = SubmitField('Submit')


class QueryForm(FlaskForm):
	postnummer = StringField("Postnummer", validators=[DataRequired()])
	afkastkrav = FloatField("Afkastkrav", validators=[RequiredIf('leje'), Optional()])
	leje = FloatField("Leje pr. m2", validators=[RequiredIf('afkastkrav'), Optional()])
	submit = SubmitField("Analyze")


class CalculatorForm(FlaskForm):
    investment_sum = FloatField("Investeringssum", validators=[DataRequired()])
    scrap_value = FloatField("Skrapværdi", validators=[DataRequired()])
    payment = FloatField("Indbetalingsbeløb", validators=[DataRequired()])
    number_of_payments = IntegerField("Antal indbetalinger", validators=[DataRequired()])
    interest = FloatField("Rente %", validators=[DataRequired()])
    pay_increase = FloatField("Forøgelse %", validators=[Optional()])
    step = IntegerField("Step", validators=[Optional(), NumberRange(min=1)])
    submit = SubmitField("Beregn")




