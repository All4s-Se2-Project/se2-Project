from App.models.review import Review
from App.database import db
from App.commands.command import Command


class CreateReviewCommand(Command):
    def __init__(self, staff, student, is_positive, rating, points, details):
        self.staff = staff
        self.student = student
        self.is_positive = is_positive
        self.rating = rating
        self.points = points
        self.details = details

    def execute(self):
        new_review = Review(
            staff=self.staff,
            student=self.student,
            is_positive=self.is_positive,
            rating=self.rating,
            points=self.points,
            details=self.details,
        )
        db.session.add(new_review)
        try:
            db.session.commit()
            return new_review
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create review: {str(e)}")


class DisplayReviewCommand(Command):
    def __init__(self, review_id):
        self.review_id = review_id

    def execute(self):
        review = Review.query.get(self.review_id)
        if not review:
            raise ValueError(f"Review with ID {self.review_id} not found")
        return review.to_json()
