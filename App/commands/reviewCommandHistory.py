from App.database import db
from App.models.ReviewCommandHistory import ReviewCommandHistory
from App.models.reviewCommand import ReviewCommand


class PushReviewCommandHistoryCommand:
    def __init__(self, review_command_id: int):
        self.review_command_id = review_command_id

    def execute(self):
        try:
            history_entry = ReviewCommandHistory(review_command_id=self.review_command_id)
            db.session.add(history_entry)
            db.session.commit()
            return history_entry
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"[PushReviewCommandHistoryCommand] Error: {str(e)}")


class PopReviewCommandHistoryCommand:
    def __init__(self, review_command_id: int):
        self.review_command_id = review_command_id

    def execute(self):
        try:
            history_entry = (
                ReviewCommandHistory.query
                .filter_by(review_command_id=self.review_command_id)
                .order_by(ReviewCommandHistory.timestamp.desc())
                .first()
            )

            if not history_entry:
                raise ValueError(f"[PopReviewCommandHistoryCommand] No history found for command_id {self.review_command_id}")

            db.session.delete(history_entry)
            db.session.commit()
            return history_entry
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"[PopReviewCommandHistoryCommand] Error: {str(e)}")


class UndoReviewCommand:
    def __init__(self, review_command_id: int):
        self.review_command_id = review_command_id

    def execute(self):
        try:
            # Pop the latest command from the history
            pop_command = PopReviewCommandHistoryCommand(self.review_command_id)
            last_command = pop_command.execute()

            if not last_command:
                raise ValueError(f"[UndoReviewCommand] No command to undo for id {self.review_command_id}")

            # Fetch the corresponding ReviewCommand for undo logic
            command = ReviewCommand.query.filter_by(id=self.review_command_id).first()
            if command and hasattr(command, 'undo'):
                command.undo()  # Assuming the `ReviewCommand` has an `undo` method
                db.session.commit()
                return True

            raise ValueError(f"[UndoReviewCommand] Command with id {self.review_command_id} not found or undo not supported")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"[UndoReviewCommand] Error: {str(e)}")
