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


def student_search(username=None, studentID=None, faculty=None, degree=None):
    query = Student.query
    if username:
        query = query.filter_by(username=username)
    if studentID:
        query = query.filter_by(ID=studentID)
    if faculty:
        query = query.filter_by(faculty=faculty)
    if degree:
        query = query.filter_by(degree=degree)
    return query.first()

def create_review(staffID, reviewType, studentName, teacher, studentID, topic, details, points):
    staff = get_staff_by_id(staffID)
    if not staff:
        raise ValueError("Staff member not found.")
    review = Review(
        reviewType=reviewType,
        studentName=studentName,
        teacher=teacher,
        studentID=studentID,
        topic=topic,
        details=details,
        points=points,
        staffID=staffID,
    )
    db.session.add(review)
    db.session.commit()
    return review

def add_rating(reviewID, rating):
    review = Review.query.get(reviewID)
    if review:
        review.rating = rating
        db.session.commit()
        return review.rating
    raise ValueError("Review not found.")

def delete_review(reviewID):
    review = Review.query.get(reviewID)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    raise ValueError("Review not found.")
