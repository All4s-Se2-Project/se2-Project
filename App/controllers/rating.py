from datetime import datetime
from App.controllers.reviewCommand import ReviewCommandController
from App.models.rating import RatingCommand
from App.models import Review
from App.models import Student
from App.database import db
from App.models import rating



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

    try:
        student.Karma += star_points
        db.session.commit()
        print(f"[rating.calculateKarma] Updated karma for Student ID {student.id} to {student.Karma}")
        return student.Karma
    except Exception as e:
        print(f"[rating.calculateKarma] Error while updating karma: {str(e)}")
        db.session.rollback()
        return None

def calculatePoints(star_rating):
    stars = {
        1: -5,
        2: -3,
        3: 1,
        4: 3,
        5: 5
    }
    return stars.get(star_rating, None)  

class RatingController(ReviewCommandController):
    def __init__(self):
        super().__init__()

    def execute(self):
       
        try:

            rating_command = Rating.query.filter_by(executed_at=None).first()  
            if not rating_command:
                print(f"[RatingController.execute] No unexecuted RatingCommand found.")
                return None

           
            rating_command.execute()


            karma_points = calculateKarma(rating_command.review_id, rating_command.star_rating)

            if karma_points is not None:
                rating_command.executed_at = datetime.utcnow()
                db.session.commit()
                print(f"[RatingController.execute] RatingCommand ID {rating_command.id} executed successfully.")
                return rating_command
            else:
                print("[RatingController.execute] Karma calculation failed.")
                return None

        except Exception as e:
            print(f"[RatingController.execute] Unexpected error: {str(e)}")
            return None

    def logChange(self):
       
        try:
            rating_command = Rating.query.filter_by(executed_at=None).first()
            if not rating_command:
                print(f"[RatingController.logChange] No executed RatingCommand found.")
                return None

            rating_command.logChange()

            db.session.commit()
            print(f"[RatingController.logChange] Changes logged for RatingCommand ID {rating_command.id}.")
            return rating_command

        except Exception as e:
            print(f"[RatingController.logChange] Unexpected error: {str(e)}")
            return None