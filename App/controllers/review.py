from App.commands.review import (
    DisplayReviewCommand,
    CreateReviewCommand,
)
from App.controllers.review import get_total_review_points


class ReviewController:
    def create_review(self, staff, student, is_positive, rating, points, details):
        try:
            command = CreateReviewCommand(staff, student, is_positive, rating, points, details)
            return command.execute()
        except ValueError as e:
            print(f"[ReviewController.create_review] Error: {str(e)}")
            return None

    def display_review(self, review_id):
        try:
            command = DisplayReviewCommand(review_id)
            return command.execute()
        except ValueError as e:
            print(f"[ReviewController.display_review] Error: {str(e)}")
            return None
