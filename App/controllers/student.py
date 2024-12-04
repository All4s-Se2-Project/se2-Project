from App.models import Student
from App.database import db


def create_student(username, UniId, firstname, lastname, email, password,
                   faculty, degree):
  newStudent = Student(username, UniId, firstname, lastname, email, password,
                       faculty, degree)
  db.session.add(newStudent)
  try:
    db.session.commit()
    return True
    # return newStudent
  except Exception as e:
    print(
        "[student.create_student] Error occurred while creating new student: ",
        str(e))
    db.session.rollback()
    return False


def get_student_by_id(id):
  student = Student.query.filter_by(id=id).first()
  if student:
    return student
  else:
    return None


def get_student_by_UniId(UniId):
  student = Student.query.filter_by(UniId=UniId).first()
  if student:
    return student
  else:
    return None


def get_student_by_username(username):
  student = Student.query.filter_by(username=username).first()
  if student:
    return student
  else:
    return None


def get_students_by_faculty(faculty):
  students = Student.query.filter_by(faculty=faculty).all()
  if students:
    return students
  else:
    return []


def get_student_for_ir(firstname, lastname, UniId):
  student = Student.query.filter_by(firstname=firstname,
                                    lastname=lastname,
                                    UniId=UniId).first()
  if student:
    return student
  else:
    return []


def get_student_by_name(firstname, lastname):
  students = Student.query.filter_by(firstname=firstname,
                                     lastname=lastname).all()
  if students:
    return students
  else:
    return []


def get_full_name_by_student_id(student_id):
    student = get_student_by_id(student_id)
    if student:
        return student.full_name  # Use the 'full_name' attribute directly
    return None



def get_students_by_degree(degree):
  students = Student.query.filter_by(degree=degree).all()
  if students:
    return students
  else:
    return []


def get_students_by_ids(student_ids):
  students = Student.query.filter(Student.ID.in_(student_ids)).all()
  return students


#returning all information about students
def get_all_students_json():
  students = Student.query.all()
  if not students:
    return []

  students_json = []
  for student in students:
    student_data = {
        'id': student.id,
        'username': student.username,
        'firstname': student.first_name,
        'lastname': student.last_name,
        'email': student.email,
        'faculty': student.faculty,
        'degree': student.degree,
        'karma': student.karma
    }
    students_json.append(student_data)

  return students_json


def update_degree(studentID, newDegree):
  student = get_student_by_id(studentID)
  if student:
    student.degree = newDegree
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[student.update_degree] Error occurred while updating student degree:",
          str(e))
      db.session.rollback()
      return False
  else:
    print(
        "[student.update_degree] Error occurred while updating student degree: Student "
        + str(studentID) + " not found")
    return False

def displayKarma(studentID):
    student = get_student_by_id(studentID)
    if not student:
        raise ValueError("Student not found.")
    return student.displayKarma()

