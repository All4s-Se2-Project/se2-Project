from App.commands.rating import CreateRatingCommand, ExecuteRatingCommand


class RatingController:
    def create_rating(self, review_id: int, rating_value: int):
        try:
            command = CreateRatingCommand(review_id, rating_value)
            return command.execute()
        except ValueError as e:
            print(f"[RatingController.create_rating] Error: {str(e)}")
            return None

    def execute_rating(self, review_id: int, star_rating: int):
        try:
            command = ExecuteRatingCommand(review_id, star_rating)
            return command.execute()
        except ValueError as e:
            print(f"[RatingController.execute_rating] Error: {str(e)}")
            return None
