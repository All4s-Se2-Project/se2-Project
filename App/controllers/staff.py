#removed old methods (staff_edit_review and staff_create_review

from App.models import Staff, Review, Student
from App.database import db 

from .review import (
    create_review,
    get_review
)
from .student import(
    get_student_by_id,
    get_student_by_username,
    get_students_by_degree,
    get_students_by_faculty
)

def create_staff(username,firstname, lastname, email, password, faculty):
    newStaff = Staff(username,firstname, lastname, email, password, faculty)
    db.session.add(newStaff)
    
    try:
        db.session.commit()
        return True
        # can return if we need
        # return newStaff
    except Exception as e:
        print("[staff.create_staff] Error occurred while creating new staff: ", str(e))
        db.session.rollback()
        return False
    

def get_staff_by_id(id):
    staff = Staff.query.filter_by(ID=id).first()
    if staff:
        return staff
    else:
        return None

def get_staff_by_name(firstname, lastname):
  staff = Staff.query.filter_by(firstname=firstname, lastname=lastname).first()
  if staff:
      return staff
  else:
      return None

def get_staff_by_username(username):
    staff = Staff.query.filter_by(username=username).first()
    if staff:
        return staff
    else:
        return None

#method for searching student
def studentSearch(self, username, studentID, faculty, degree):
    return Student.query.filter_by(
        username=username, 
        ID=studentID, 
        faculty=faculty, 
        degree=degree
    ).first()

#method for creating a review
def createReview(self, reviewType, studentName, teacher, studentID, topic, details, points):
    review = Review(
        reviewType=reviewType,
        studentName=studentName,
        teacher=teacher,
        studentID=studentID,
        topic=topic,
        details=details,
        points=points,
        staffID=self.ID
    )
    db.session.add(review)
    db.session.commit()
    return review

#method to add rating
def addRating(self, ReviewID, rating):
    review = Review.query.get(ReviewID)
    if review:
        review.rating = rating
        db.session.commit()
        return review.rating
    raise ValueError("Review not found.")

#method to delete review
def deleteReview(self, ReviewID):
    review = Review.query.get(ReviewID)

    if review:
        db.session.delete(review)
        db.session.commit()

