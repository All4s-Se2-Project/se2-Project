from App.commands.review import (
    DisplayReviewCommand,
    CreateReviewCommand,
)
#from App.controllers.review import get_total_review_points

class ReviewController:
    #not in use, try to remove safely
    @staticmethod
    def create_review(staff, student, is_positive, rating, points, details):
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
    
    #not in use, try to remove safely    
    @staticmethod
    def get_total_review_points(reviews):
        #for testing purposes
        pass
