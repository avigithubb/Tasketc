from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, EmailField
from wtforms.validators import DataRequired, URL

class Registration_form(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Your Name"})
    email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "example@gmail.com"})
    password = StringField("Password", validators=[DataRequired()], render_kw={"placeholder": "must be 8 characters or more"})
    submit = SubmitField("Register me")

class Login_form(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "eg@gmail.com"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Your password"})
    submit = SubmitField("Log me in")

class Item_Entry_form(FlaskForm):
    title = StringField("", render_kw={"value": "List_title_here", "maxlength": 15, "size": 15, "class": "create_input"})
    image = StringField("",validators=[URL()], render_kw={"type": "image", "src": "{{ url_for('static', filename='images/icons8-edit-64.png') }}", "width": "5px", "height": "5px", "class": "input_img"})
    textarea = TextAreaField("", render_kw={"placeholder": "For eg. Buy Bacon..", "cols":55, "rows":10})
    submit_btn = SubmitField("", render_kw={"value": "Add item", "id": "submit-button", "type": "button"})
