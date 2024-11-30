from App.models import ReviewCommand
from App.database import db
from datetime import datetime


class ReviewCommandController:
    def execute(self):
        try:
            review_command = ReviewCommand.query.order_by(ReviewCommand.executed_at.desc()).first()
            
            if not review_command:
                print("[ReviewCommandController.execute] No ReviewCommand found.")
                return None
            
            review_command.execute()  
            
            
            review_command.executed_at = datetime.utcnow()
            db.session.commit()
            print(f"[ReviewCommandController.execute] Executed ReviewCommand ID {review_command.id} successfully.")
            return review_command
        except Exception as e:
            print(f"[ReviewCommandController.execute] Unexpected error: {str(e)}")
            return None

    def logChange(self):
        try:
            review_command = ReviewCommand.query.order_by(ReviewCommand.executed_at.desc()).first()
            
            if not review_command:
                print("[ReviewCommandController.logChange] No ReviewCommand found.")
                return None
            
            
            review_command.logChange()  
            
            
            db.session.commit()
            print(f"[ReviewCommandController.logChange] Changes logged for ReviewCommand ID {review_command.id}.")
            return review_command
        except Exception as e:
            print(f"[ReviewCommandController.logChange] Unexpected error: {str(e)}")
            return None
