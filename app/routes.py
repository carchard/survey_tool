from app import app, json_fname, results_fname
from app.survey_form import GenericSurvey
from app.data_management import record_form, init_results, show_results
from flask import render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired

import json
import logging
import os

init_results() 

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    logging.warn("about to open json file at: {}".format(os.path.abspath(json_fname)))

    # parse the current survey
    with open(json_fname, 'rb') as f:
        survey_form = json.load(f)

    questions = survey_form.get('questions', [])
    title = survey_form.get('title', 'Missing Title')

    # edit the form class based on question types
    for idx, q in enumerate(questions):
        attr_key = 'q{}'.format(idx)

        if q['type'] == 'short_answer':
            setattr(GenericSurvey, attr_key, StringField(q['text'],
                validators=[DataRequired()]))
            
        elif q['type'] == '1-5':
            setattr(GenericSurvey, attr_key, RadioField(q['text'], 
                choices=[(x, str(x)) for x in range(1, 6)],
                coerce=int,
                validators=[DataRequired()]))
            
        elif q['type'] == 'yes_no':
            setattr(GenericSurvey, attr_key, RadioField(q['text'], 
                choices=[(2, 'yes'), (1, 'no')],
                coerce=int,
                validators=[DataRequired()]))
            
        elif q['type'] == '1-10':
            setattr(GenericSurvey, attr_key, RadioField(q['text'], 
                choices=[(x, str(x)) for x in range(1, 11)],
                coerce=int,
                validators=[DataRequired()]))

        elif q['type'] == 'long_answer':
            setattr(GenericSurvey, attr_key, TextAreaField(q['text'],
                validators=[DataRequired()]))  

        elif q['type'] == 'long_answer_optional':
            setattr(GenericSurvey, attr_key, TextAreaField(q['text'],
                validators=[]))  

        elif q['type'] == 'disagree_agree':
            setattr(GenericSurvey, attr_key, RadioField(q['text'],
                choices=[(1, 'strongly disagree'), (2, 'disagree'), (3, 'neutral'), (4, 'agree'), (5, 'strongly agree')],
                coerce=int,
                validators=[DataRequired()]))            

        else:
            setattr(GenericSurvey, attr_key, StringField(q['text'],
                validators=[DataRequired()]))

    form = GenericSurvey()

    print(form.errors)
    if form.validate_on_submit():
        flash('Survey Submitted!')
        record_form(form, questions=questions)
        return redirect('/results')

    return render_template('index.html', 
        title=title, 
        questions=questions,
        form=form)


@app.route('/results')
def results():
    title, results_list = show_results()
    return render_template('results.html', 
        title=title, 
        results_list=results_list)
