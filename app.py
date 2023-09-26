#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import datetime
from distutils.command.install_lib import PYTHON_SOURCE_EXTENSION
from email.policy import default
from math import factorial
from os import urandom
import dateutil.parser
import babel
from flask import Flask, abort, render_template, request, Response, flash, redirect, url_for, jsonify
from jinja2.utils import markupsafe
from flask_moment import Moment
from flask import request
import logging
import os
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
from sqlalchemy import desc
from settings import app, db
from models import db, Items, Questions, Section, Item_type, Job
#----------------------------------------------------------------------

# -----------------------------------------------------------------

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/', methods=['GET'])
def index():
  return render_template('pages/home.html')

@app.route('/items', methods=['GET'])
def all_items():
  results = Questions.query.all()
  items = []

  for item in results:
    result = {}
    result["question"] = item.stem
    result["A"] = item.A
    result["B"] = item.B
    result["C"] = item.C
    result["D"] = item.D
    result["answer"] = item.answer
    result["xml_ref_main"] = item.xml_ref_main
    result["final_rubric"] = item.final_rubric

    items.append(result)
  
  return render_template('pages/items.html', items=items)

@app.route('/items/<string:xml_ref_main>/view', methods=['GET'])
def item(xml_ref_main):
  results = Items.query.get(xml_ref_main)
  question = Questions.query.get(xml_ref_main)
  items = []
  result = {}

  result["stem"] = question.stem
  result["A"] = question.A
  result["B"] = question.B
  result["C"] = question.C
  result["D"] = question.D
  result["answer"] = question.answer
  result["xml_ref_main"] = results.xml_ref_main
  result["xml_ref_sub"] = question.xml_ref_sub
  result["xml_objective"] = results.xml_objective
  result["section"] = results.section 
  result["job"] = results.job 
  result["item_type"] =  results.item_type
  result["item_number"] = question.item_number
  result["question_number"] = question.question_number 
  result["can_do_skill"] =results.can_do_skill 
  result["uploaded_by"] = results.uploaded_by 
  result["grammar"] = results.grammar
  result["objective_no"] = results.objective_no
  result["congruence"] = results.congruence
  result["scoring"] = question.scoring
  result["reference"] = results.reference 
  result["rubric_part_1"] = results.rubric_part_1 
  result["rubric_part_2"] = results.rubric_part_2 
  result["final_rubric"] = question.final_rubric
  result["rat_opt_a"] = question.rat_opt_a 
  result["rat_opt_b"] = question.rat_opt_b
  result["rat_opt_c"] = question.rat_opt_c
  result["rat_opt_d"] = question.rat_opt_d
  result["notes"] = results.notes

  items.append(result)
  
  return render_template('pages/item.html', items=items)

@app.route('/items/create', methods=['GET'])
def create_item_form():
  form = ItemForm()
  return render_template('forms/new_item.html', form=form)

@app.route('/items/create', methods=['POST'])
def create_item_submission():  
  # Request data from the Item Form
  if request.method == "POST":
    form = ItemForm()

    item_dict = {}
    form_section = form.section.data,
    form_job = form.job.data,
    form_item_type = form.item_type.data,
    question_number = form.question_number.data
    item_number = form.item_number.data
    exam_level = "B15"
    # item_type = ""
    # job = ""
    # section = ""

    # Section
    if "Use of English" in form_section:
      item_dict["section"] = "UOE"
    elif "Listening" in form_section:
      item_dict["section"] = "L"
    elif "Reading" in form_section:
      item_dict["section"] = "R"
    elif "Writing" in form_section:
      item_dict["section"] = "W"
    elif "Speaking" in form_section:
      item_dict["section"] = "S"

    # Job
    if "Customer Support" in form_job:
      item_dict["job"] = "CS"
    elif "Product Manager" in form_job:
      item_dict["job"] = "PM"
    elif "Network Engineer" in form_job:
      item_dict["job"] = "NE"
    elif "Security Engineer" in form_job:
      item_dict["job"] = "SEC"
    elif "Software Developer" in form_job:
      item_dict["job"] = "SOF"

    # Question Type
    if "Multiple Choice Selection" in form_item_type:
      item_dict["item_type"] = "MCS"
    elif "Prompt & Reply" in form_item_type:
      item_dict["item_type"] = "PR"
    elif "Multiple Choice Cloze" in form_item_type:
      item_dict["item_type"] = "MCC"
    elif "Opinion Matching" in form_item_type:
      item_dict["item_type"] = "OM"
    elif "Multiple Matching" in form_item_type:
      item_dict["item_type"] = "MM"
    elif "Longer Multiple Choice" in form_item_type:
      item_dict["item_type"] = "LMC"
    elif "Statement Agreement" in form_item_type:
      item_dict["item_type"] = "SA"
    elif "Listening Multiple Choice Selection" in form_item_type:
      item_dict["item_type"] = "MCS"


    xml_ref_main = "{}_{}_{}_{}_0{}".format(exam_level, item_dict["section"], item_dict["job"], item_dict["item_type"], question_number)
    xml_ref_sub = "{}_0{}".format(xml_ref_main, item_number)
    
    db_item = Questions.query.get(xml_ref_main)

    if db_item and db_item.xml_ref_sub == xml_ref_sub:
      flash('Item "{}" already exists'.format(xml_ref_main))
      db.session.rollback()
      return redirect(url_for('all_items'))
    else:
      item = Items(
        xml_ref_main = xml_ref_main,
        xml_objective = form.xml_objective.data,
        section = form_section,
        job = form_job,
        item_type = form_item_type,
        can_do_skill = form.can_do_skill.data,
        uploaded_by = form.uploaded_by.data,
        grammar = form.grammar.data,
        objective_no = form.objective_no.data,
        congruence = form.congruence.data,
        reference = form.reference.data,
        script_text = form.script_text.data,
        rubric_part_1 = form.rubric_part_1.data,
        rubric_part_2 = form.rubric_part_2.data,
        notes = form.notes.data
      )
      question = Questions(
        xml_ref_main = xml_ref_main,
        xml_ref_sub = xml_ref_sub,
        question_number = form.question_number.data,
        item_number = form.item_number.data,
        final_rubric = form.final_rubric.data,
        stem = form.stem.data,
        A = form.A.data,
        B = form.B.data,
        C = form.C.data,
        D = form.D.data,
        rat_opt_a = form.rat_opt_a.data,
        rat_opt_b = form.rat_opt_b.data,
        rat_opt_c = form.rat_opt_c.data,
        rat_opt_d = form.rat_opt_d.data,
        answer = form.answer.data,
        scoring = form.scoring.data,
      )
      # Add and commit the received form input
      db.session.add(item)
      db.session.add(question)
      db.session.commit()
      flash('Item "{}" was successfully listed!'.format(xml_ref_main))
      db.session.close()
      return redirect(url_for('all_items'))
  else:
    flash('An error occurred. Item "{}" could not be listed!'.format(xml_ref_main))
    db.session.rollback()
    return redirect(url_for('all_items'))

@app.route('/items/<string:xml_ref_main>/edit', methods=['GET'])
def edit_form_item(xml_ref_main):
  item = Items.query.get(xml_ref_main)
  question = Questions.query.get(xml_ref_main)
  form = ItemForm(obj=item)
  form2 = ItemForm(obj=question)
  return render_template('forms/update_item.html', form=form, form2=form2, item=item, question=question)

@app.route('/items/<string:xml_ref_main>/edit', methods=['POST'])
def edit_item(xml_ref_main):
  form = ItemForm(request.form)
  if request.method == "POST":
    item = Items.query.get(xml_ref_main)
    
    item.xml_objective = form.xml_objective.data,
    item.section = form.section.data,
    item.job = form.job.data,
    item.item_type = form.item_type.data,
    item.can_do_skill = form.can_do_skill.data,
    item.uploaded_by = form.uploaded_by.data,
    item.grammar = form.grammar.data,
    item.objective_no = form.objective_no.data,
    item.congruence = form.congruence.data,
    item.reference = form.reference.data,
    item.script_text = form.script_text.data,
    item.rubric_part_1 = form.rubric_part_1.data,
    item.rubric_part_2 = form.rubric_part_2.data,
    item.notes = form.notes.data

    question = Questions.query.get(xml_ref_main)
    question.question_number = form.question_number.data,
    question.item_number = form.item_number.data,
    question.final_rubric = form.final_rubric.data,
    question.stem = form.stem.data,
    question.A = form.A.data,
    question.B = form.B.data,
    question.C = form.C.data,
    question.D = form.D.data,
    question.rat_opt_a = form.rat_opt_a.data,
    question.rat_opt_b = form.rat_opt_b.data,
    question.rat_opt_c = form.rat_opt_c.data,
    question.rat_opt_d = form.rat_opt_d.data,
    question.answer = form.answer.data,
    question.scoring = form.scoring.data,

    # Add and commit the received form input
    db.session.add(item)
    db.session.add(question)
    db.session.commit()
    flash('Item ' + xml_ref_main + ' was successfully updated!')
    db.session.close()
    return redirect(url_for('all_items'))
  else:
    flash('An error occurred. Item ' + xml_ref_main + ' could not be updated!')
    db.session.rollback()
  
  return redirect(url_for('all_items'))

@app.route('/items/<string:xml_ref_main>/delete', methods=['GET'])
def delete_item(xml_ref_main):
  if request.method == 'GET':
    item = Items.query.get(xml_ref_main)
    question = Questions.query.get(xml_ref_main)
    db.session.delete(item)
    db.session.delete(question)
    db.session.commit()
    flash('Item has been deleted successfully')
    
  else:
    db.session.rollback
    flash('Unsuccesful attenpt to delete item')
    db.session.close()
  
  return redirect(url_for('all_items'))

# Get all sections
@app.route('/sections', methods=['GET'])
def show_sections():
  # Query the section table
  items = Section.query.all()
  
  return render_template('pages/sections.html', items=items)

# Create new section 
@app.route('/sections/create', methods=['GET'])
def create_section_form():
  form = ItemForm()
  return render_template('forms/new_section.html', form=form)

@app.route('/sections/create', methods=['POST'])
def create_section_submission():
  
  # Request data from the Item Form
  if request.method == "POST":
    form = ItemForm()
    item_name = form.new_section.data
    split_name = item_name.split()

    id = "".join(split_name)
    db_item = Section.query.get(id)

    if db_item:
      flash(item_name + ' already exists')
      db.session.rollback()
      return redirect(url_for('show_sections'))

    else:
      item = Section(
        name = item_name,
        id = "".join(split_name)
      )

    # Add and commit the received form input
      db.session.add(item)
      db.session.commit()
      flash('Item was successfully listed!')

      db.session.close()
      return redirect(url_for('show_sections'))
  else:
    flash('An error occurred. Item could not be listed!')
    db.session.rollback()
  
  return redirect(url_for('show_sections'))

@app.route('/sections/<string:id>', methods=['GET'])
def section_item(id):
  section = Section.query.get(id)
  section_name = section.name
  # Query the Questions table by section
  results = Items.query.filter(Items.section.ilike('%{}%'.format(section_name))).all()
  items = []

  for item in results:
    result = {}
    result["section_id"] = section.id
    xml_ref_main = item.xml_ref_main
    result["xml_ref_main"] = xml_ref_main
    question = Questions.query.get(xml_ref_main)
    result["final_rubric"] = question.final_rubric
    result["stem"] = question.stem
    result["A"] = question.A
    result["B"] = question.B
    result["C"] = question.C
    result["D"] = question.D

    items.append(result)
  
  return render_template('pages/section.html', items=items)

@app.route('/section/<string:id>/delete', methods=['GET'])
def delete_section(id):
  if request.method == 'GET':
    item = Section.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted successfully')
    
  else:
    db.session.rollback
    flash('Unsuccesful attenpt to delete item')
    db.session.close()
  
  return redirect(url_for('show_sections'))

@app.route('/jobs', methods=['GET'])
def show_jobs():
  # Query the jobs table
  items = Job.query.all()
  
  return render_template('pages/jobs.html', items=items)

# Create new job
@app.route('/jobs/create', methods=['GET'])
def create_job_form():
  form = ItemForm()
  return render_template('forms/new_job.html', form=form)

@app.route('/jobs/create', methods=['POST'])
def create_job_submission():
  
  # Request data from the Item Form
  if request.method == "POST":
    form = ItemForm()
    item_name = form.new_job.data
    split_name = item_name.split()

    id = "".join(split_name)
    db_item = Job.query.get(id)

    if db_item:
      flash(item_name + ' already exists')
      db.session.rollback()
      return redirect(url_for('show_jobs'))

    else:
      item = Job(
        name = item_name,
        id = "".join(split_name)
      )

    # Add and commit the received form input
      db.session.add(item)
      db.session.commit()
      flash('Item was successfully listed!')

      db.session.close()
      return redirect(url_for('show_jobs'))
  else:
    flash('An error occurred. Item could not be listed!')
    db.session.rollback()
  
  return redirect(url_for('show_jobs'))


@app.route('/jobs/<string:id>', methods=['GET'])
def job_item(id):
  job = Job.query.get(id)
  job_name = job.name
  # Query the Questions table by section
  results = Items.query.filter(Items.job.ilike('%{}%'.format(job_name))).all()
  items = []

  for item in results:
    result = {}
    xml_ref_main = item.xml_ref_main
    result["job_id"] = job.id
    result["xml_ref_main"] = xml_ref_main
    question = Questions.query.get(xml_ref_main)
    result["final_rubric"] = question.final_rubric
    result["stem"] = question.stem
    result["A"] = question.A
    result["B"] = question.B
    result["C"] = question.C
    result["D"] = question.D

    items.append(result)
  
  return render_template('pages/job.html', items=items)

@app.route('/jobs/<string:id>/delete', methods=['GET'])
def delete_job(id):
  if request.method == 'GET':
    item = Job.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted successfully')
    
  else:
    db.session.rollback
    flash('Unsuccesful attenpt to delete item')
    db.session.close()
  
  return redirect(url_for('show_jobs'))

@app.route('/item_types', methods=['GET'])
def show_item_types():
  # Query the item_Type table by the id
  items = Item_type.query.all()
  
  return render_template('pages/item_types.html', items=items)

# Create new item type
@app.route('/item_types/create', methods=['GET'])
def create_item_type_form():
  form = ItemForm()
  return render_template('forms/new_item_type.html', form=form)

@app.route('/item_types/create', methods=['POST'])
def create_item_type_submission():
  
  # Request data from the Item Form
  if request.method == "POST":
    form = ItemForm()
    item_name = form.new_item_type.data
    split_name = item_name.split()

    id = "".join(split_name)
    db_item = Item_type.query.get(id)

    if db_item:
      flash(item_name + ' already exists')
      db.session.rollback()
      return redirect(url_for('show_item_types'))

    else:
      item = Item_type(
        name = item_name,
        id = "".join(split_name)
      )

    # Add and commit the received form input
      db.session.add(item)
      db.session.commit()
      flash('Item was successfully listed!')

      db.session.close()
      return redirect(url_for('show_item_types'))
  else:
    flash('An error occurred. Item could not be listed!')
    db.session.rollback()
  
  return redirect(url_for('show_item_types'))

@app.route('/item_types/<string:id>', methods=['GET'])
def show_item_type(id):
  item_type = Item_type.query.get(id)
  item_name = item_type.name
  # Query the Questions table by section
  results = Items.query.filter(Items.item_type.ilike('%{}%'.format(item_name))).all()
  items = []

  for item in results:
    result = {}
    xml_ref_main = item.xml_ref_main
    result["item_type_id"] = item_type.id
    result["xml_ref_main"] = xml_ref_main
    question = Questions.query.get(xml_ref_main)
    result["final_rubric"] = question.final_rubric
    result["stem"] = question.stem
    result["A"] = question.A
    result["B"] = question.B
    result["C"] = question.C
    result["D"] = question.D

    items.append(result)
  
  return render_template('pages/item_type.html', items=items)

@app.route('/section/<string:id>/delete', methods=['GET'])
def delete_item_type(id):
  if request.method == 'GET':
    item = Item_type.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted successfully')
    
  else:
    db.session.rollback
    flash('Unsuccesful attenpt to delete item')
    db.session.close()
  
  return redirect(url_for('show_item_types'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
