from App.commands.reviewCommand import (
    CreateReviewCommand,
    UndoReviewCommand,
    ExecuteReviewCommand,
)


class ReviewCommandController:
    def create_review_command(self, review_id: int, command_type: str):
        try:
            command = CreateReviewCommand(review_id, command_type)
            return command.execute()
        except ValueError as e:
            print(f"[ReviewCommandController.create] Error: {str(e)}")
            return None

    def execute_review_command(self, review_command_id: int):
        try:
            command = ExecuteReviewCommand(review_command_id)
            return command.execute()
        except ValueError as e:
            print(f"[ReviewCommandController.execute] Error: {str(e)}")
            return None

    def undo_review_command(self, review_command_id: int):
        try:
            command = UndoReviewCommand(review_command_id)
            return command.execute()
        except ValueError as e:
            print(f"[ReviewCommandController.undo] Error: {str(e)}")
            return None
