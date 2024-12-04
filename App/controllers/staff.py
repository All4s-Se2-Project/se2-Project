from App.controllers.student import get_student_by_UniId, get_student_by_id
from App.models import Staff, Review, Student
from App.database import db


def create_staff(username, firstname, lastname, email, password, faculty):
    newStaff = Staff(username, firstname, lastname, email, password, faculty)
    db.session.add(newStaff)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[staff.create_staff] Error occurred while creating new staff: ", str(e))
        db.session.rollback()
        return False

def get_staff_by_id(id):
    return Staff.query.filter_by(id=id).first()

def get_staff_by_name(firstname, lastname):
    return Staff.query.filter_by(first_name=firstname, last_name=lastname).first()

def get_staff_by_username(username):
    return Staff.query.filter_by(username=username).first()


def student_search(username=None, UniId=None, faculty=None, degree=None):
    query = Student.query
    if username:
        query = query.filter_by(username=username)
    if UniId:
        query = query.filter_by(UniId=UniId)
    if faculty:
        query = query.filter_by(faculty=faculty)
    if degree:
        query = query.filter_by(degree=degree)
    return query.first()

def create_review(staffID, is_positive, UniId, rating, details): 
    staff = get_staff_by_id(staffID)
    if not staff:
        raise ValueError("Staff member not found.")

    student = get_student_by_UniId(UniId)  
    if not student:
        raise ValueError("Student not found.")
    
    # Calculate points based on rating
    if rating == 1:
        points = -5
    elif rating == 2:
        points = -3
    elif rating == 3:
        points = 1
    elif rating == 4:
        points = 3
    elif rating == 5:
        points = 5
    else:
        raise ValueError("Invalid rating. Rating must be between 1 and 5.")

    review = Review(
        staff=staff,
        student=student,
        is_positive=is_positive,
        rating=rating,
        points=points,
        details=details,
    )
    db.session.add(review)
    db.session.commit()
    return review

def get_review(reviewID):
    review = Review.query.get(reviewID)
    if review:
        return review
    else:
        return None

def delete_review(reviewID):
    review = get_review(reviewID)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    raise ValueError("Review not found.")

