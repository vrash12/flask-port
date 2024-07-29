from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    tags = StringField('Tags')  # Optional
    body = TextAreaField('Body', validators=[DataRequired()])
    image = StringField('Image URL')  # You can use a FileField for actual file uploads
    submit = SubmitField('Post')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    technologies = StringField('Technologies')
    image = StringField('Image URL')
    submit = SubmitField('Submit')