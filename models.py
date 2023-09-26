from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Create items table
class Items(db.Model):
  __tablename__ = 'items'

  xml_ref_main = db.Column(db.String, primary_key=True)
  xml_objective = db.Column(db.String(500))
  section = db.Column(db.String(500))
  job = db.Column(db.String(500))
  item_type = db.Column(db.String(500))
  sub_ref_number = db.Column(db.String())
  can_do_skill = db.Column(db.String(500))
  uploaded_by = db.Column(db.String(db.String(500)))
  grammar = db.Column(db.String(500))
  objective_no = db.Column(db.String())
  sub_obj_no = db.Column(db.String())
  congruence = db.Column(db.String(500))
  reference = db.Column(db.String(500))
  script_text = db.Column(db.String(1000))
  rubric_part_1 = db.Column(db.String(500))
  rubric_part_2 = db.Column(db.String(500))
  notes = db.Column(db.String(1500))
 
# Create questions table
class Questions(db.Model):
  __tablename__ = 'questions'

  xml_ref_main = db.Column(db.String, primary_key=True)
  xml_ref_sub = db.Column(db.String(1000))
  question_number = db.Column(db.String())
  item_number = db.Column(db.String())
  final_rubric = db.Column(db.String(1000))
  stem = db.Column(db.String(1000))
  A = db.Column(db.String(500))
  B = db.Column(db.String(500))
  C = db.Column(db.String(500))
  D = db.Column(db.String(500))
  answer = db.Column(db.String(500))
  scoring = db.Column(db.String(500))
  rat_opt_a = db.Column(db.String(500))
  rat_opt_b = db.Column(db.String(500))
  rat_opt_c = db.Column(db.String(500))
  rat_opt_d = db.Column(db.String(500))

class Section(db.Model):
  __tablename__ = 'section'

  id = db.Column(db.String(120), primary_key=True)
  name = db.Column(db.String(120))

class Job(db.Model):
  __tablename__ = 'job'

  id = db.Column(db.String(120), primary_key=True)
  name = db.Column(db.String(120))

class Item_type(db.Model, ):
  __tablename__ = 'item_type'

  id = db.Column(db.String(120), primary_key=True)
  name = db.Column(db.String(120))
  