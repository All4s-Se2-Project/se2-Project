from App.models.rating import RatingCommand
from App.models import Review
from App.models import Student
from App.database import db


def createRating(reviewID, rating_value):
    newRating= RatingCommand(reviewID, rating_value)
    db.session.add(newRating)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(
            "[rating.createRating] Error occurred while creating new rating: ",
            str(e))
        db.session.rollback()
        return False 

def execute(reviewID, star_rating):
    calculateKarma(reviewID, star_rating)

def calculatePoints(star_rating):
    stars= {
        1: -5,
        2: -3,
        3: 1,
        4: 3,
        5: 5
    }
    #int_star_rating= int(star_rating)
    if star_rating in stars:
        return stars[star_rating]
    else:
        return None


def calculateKarma(reviewID, star_rating):
    star_points= calculatePoints(star_rating)
    review= Review.query.filter_by(ID=reviewID).first()
    student= Student.query.filter_by(ID=review.studentID).first()
    star_points = calculatePoints(star_rating)
    if star_points is None:
        print("[rating.calculateKarma] Invalid star rating provided")
        return None

    if review is None or student is None:
     review = Review.query.filter_by(id=reviewID).first()
    if review is None:
        print(f"[rating.calculateKarma] Review with ID {reviewID} not found")
        return None
    student = Student.query.filter_by(id=review.student_id).first()
    if student is None:
        print(f"[rating.calculateKarma] Student with ID {review.student_id} not found")
        return None
    student.karmaPoints += star_points
    db.session.commit()
    return student.karmaPoints
    # Update the student's karma
    try:
        student.Karma += star_points
        db.session.commit()
        print(f"[rating.calculateKarma] Updated karma for Student ID {student.id} to {student.Karma}")
        return student.Karma
    except Exception as e:
        print(f"[rating.calculateKarma] Error while updating karma: {str(e)}")
        db.session.rollback()
        return None


def logChange():
    pass