from App.models.rating import RatingCommand
from App.models.review import Review
from App.models.student import Student
from App.database import db


class CreateRatingCommand:
    def __init__(self, review_id: int, rating_value: int):
        self.review_id = review_id
        self.rating_value = rating_value

    def execute(self):
        new_rating = RatingCommand(self.review_id, self.rating_value)
        db.session.add(new_rating)
        try:
            db.session.commit()
            return new_rating
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"[CreateRatingCommand] Error: {str(e)}")


class CalculateKarmaCommand:
    def __init__(self, review_id: int, star_rating: int):
        self.review_id = review_id
        self.star_rating = star_rating

    @staticmethod
    def calculate_points(star_rating):
        points_map = {1: -5,
                      2: -3,
                      3: 1,
                      4: 3,
                      5: 5}
        return points_map.get(star_rating, 0)

    def execute(self):
        review = Review.query.filter_by(id=self.review_id).first()
        if not review:
            raise ValueError(f"[CalculateKarmaCommand] Review with ID {self.review_id} not found.")

        student = Student.query.filter_by(ID=review.student_id).first()
        if not student:
            raise ValueError(f"[CalculateKarmaCommand] Student for review ID {self.review_id} not found.")

        star_points = self.calculate_points(self.star_rating)
        student.karmaPoints += star_points

        try:
            db.session.commit()
            return student.karmaPoints
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"[CalculateKarmaCommand] Error updating karma: {str(e)}")


class ExecuteRatingCommand:
    def __init__(self, review_id: int, star_rating: int):
        self.review_id = review_id
        self.star_rating = star_rating

    def execute(self):
        return CalculateKarmaCommand(self.review_id, self.star_rating).execute()
