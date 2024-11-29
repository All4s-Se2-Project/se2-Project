from App.commands.reviewCommandHistory import (
    PushReviewCommandHistoryCommand,
    PopReviewCommandHistoryCommand,
    UndoReviewCommand,
)


class ReviewCommandHistoryController:
    def push_review_command_history(self, review_command_id: int):
        try:
            command = PushReviewCommandHistoryCommand(review_command_id)
            return command.execute()
        except ValueError as e:
            print(f"[ReviewCommandHistoryController.push] Error: {str(e)}")
            return None

    def pop_review_command_history(self, review_command_id: int):
        try:
            command = PopReviewCommandHistoryCommand(review_command_id)
            return command.execute()
        except ValueError as e:
            print(f"[ReviewCommandHistoryController.pop] Error: {str(e)}")
            return None

    def undo_review_command(self, review_command_id: int):
        try:
            command = UndoReviewCommand(review_command_id)
            return command.execute()
        except ValueError as e:
            print(f"[ReviewCommandHistoryController.undo] Error: {str(e)}")
            return None
