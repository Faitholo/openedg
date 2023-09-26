from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, AnyOf, URL

class ItemForm(Form):
    xml_objective = StringField(
        'xml_objective'
    )
    section = SelectField(
        'section', validators=[DataRequired()],
        choices=[
            ("Use of English", "Use of English"),
            ("Listening", "Listening"),
            ("Reading", "Reading"),
            ("Writing", "Writing"),
            ("Speaking", "Speaking"),
        ]
    )
    job = SelectField(
        'job', validators=[DataRequired()],
        choices=[
            ("Customer Support", "Customer Support"),
            ("Product Manager", "Product Manager"),
            ("Network Engineer", "Network Engineer"),
            ("Security Engineer", "Security Engineer"),
            ("Software Developer", "Software Developer"),
        ]
    )
    item_type = SelectField(
        'item_type', validators=[DataRequired()],
        choices=[
            ("Multiple Choice Selection", "Multiple Choice Selection"),
            ("Prompt & Reply", "Prompt & Reply"),
            ("Multiple Choice Cloze", "Multiple Choice Cloze"),
            ("Opinion Matching", "Option Matching"),
            ("Multiple Matching", "Multiple Matching"),
            ("Longer Multiple Matching", "Longer Multiple Matching"),
            ("Statement Agreement", "Statement Agreement"),
            ("Listening Multiple Choice Selection", "Listening Multiple Choice Selection")
        ]
    )
    item_number = IntegerField(
        'reference_number', validators=[DataRequired()]
    )
    question_number = IntegerField(
        'question_number', validators=[DataRequired()]
    )
    can_do_skill = StringField(
        'can_do_skill'
    )
    uploaded_by = StringField(
        'uploaded_by'
    )
    grammar = StringField(
        'grammar'
    )
    objective_no = StringField(
        'objective_no'
    )
    reference = StringField(
        'reference', validators=[URL()]
    )
    congruence = StringField(
        'congruence'
    )
    script_text = TextAreaField(
         'script_text'
    )
    rubric_part_1 = TextAreaField(
        'rubric_part_1'
    )
    rubric_part_2 = TextAreaField(
        'rubric_part_2'
    )
    final_rubric = TextAreaField(
        'final_rubric'
    )
    notes = TextAreaField(
        'notes'
    )
    question_number = StringField(
        'question_number', validators=[DataRequired()]
    )
    stem = TextAreaField(
        'stem', validators=[DataRequired()]
    )
    A = StringField(
        'A'
    )
    B = StringField(
        'B'
    )
    C = StringField(
        'C'
    )
    D = StringField(
        'D'
    )
    rat_opt_a = StringField(
        'rat_opt_a'
    )
    rat_opt_b = StringField(
        'rat_opt_b'
    )
    rat_opt_c = StringField(
        'rat_opt_c'
    )
    rat_opt_d = StringField(
        'rat_opt_d'
    )
    answer = SelectField(
        'answer',
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D")
        ]
    )
    scoring = StringField(
        'scoring'
    )
    new_section = StringField(
        'new_section'
    )
    new_job = StringField(
        'new_job'
    )
    new_item_type = StringField(
        'new_item_type'
    )

