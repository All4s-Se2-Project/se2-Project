from App.database import db
from App.models.reviewCommand import ReviewCommand
from App.models.ReviewCommandHistory import ReviewCommandHistory


class CreateReviewCommand:
    def __init__(self, review_id: int, command_type: str):
        self.review_id = review_id
        self.command_type = command_type

    def execute(self):
        try:
            new_command = ReviewCommand(review_id=self.review_id, command_type=self.command_type)
            db.session.add(new_command)
            db.session.commit()

            # Push to history
            history_entry = ReviewCommandHistory(review_command_id=new_command.id)
            db.session.add(history_entry)
            db.session.commit()

            return new_command
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"[CreateReviewCommand] Error: {str(e)}")


class ExecuteReviewCommand:
    def __init__(self, review_command_id: int):
        self.review_command_id = review_command_id

    def execute(self):
        try:
            command = ReviewCommand.query.filter_by(id=self.review_command_id).first()
            if not command:
                raise ValueError(f"ReviewCommand with ID {self.review_command_id} not found")

            command.execute()
            return command
        except Exception as e:
            raise ValueError(f"[ExecuteReviewCommand] Error: {str(e)}")


class UndoReviewCommand:
    def __init__(self, review_command_id: int):
        self.review_command_id = review_command_id

    def execute(self):
        try:
            # Fetch the command from the database
            command = ReviewCommand.query.filter_by(id=self.review_command_id).first()
            if not command:
                raise ValueError(f"ReviewCommand with ID {self.review_command_id} not found")

            # Undo the command
            command.undo()

            # Remove from history
            history_entry = ReviewCommandHistory.query.filter_by(review_command_id=self.review_command_id).first()
            if history_entry:
                db.session.delete(history_entry)
                db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"[UndoReviewCommand] Error: {str(e)}")
