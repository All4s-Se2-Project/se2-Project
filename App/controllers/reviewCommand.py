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

        try:
            review_command.execute()  
        except NotImplementedError:
            print(f"[ReviewCommandController.execute] No custom execute logic for command type: {review_command.command_type}.")
        
        review_command.executed_at = datetime.utcnow()  
        db.session.commit()
        print(f"[ReviewCommandController.execute] Executed ReviewCommand ID {review_command.id} successfully.")
        return review_command
    except Exception as e:
        print(f"[ReviewCommandController.execute] Unexpected error: {str(e)}")
        return None

   def logChange(self):
    '''try:
        review_command = ReviewCommand.query.order_by(ReviewCommand.executed_at.desc()).first()

        if not review_command:
            print("[ReviewCommandController.logChange] No ReviewCommand found.")
            return None

        try:
            review_command.logChange()  
        except NotImplementedError:
            print(f"[ReviewCommandController.logChange] No custom log logic for command type: {review_command.command_type}. Default logging applied.")
            
            print(f"Default log: Command ID {review_command.id}, Type {review_command.command_type}.")

        db.session.commit()
        print(f"[ReviewCommandController.logChange] Changes logged for ReviewCommand ID {review_command.id}.")
        return review_command
    except Exception as e:
        print(f"[ReviewCommandController.logChange] Unexpected error: {str(e)}")
        return None'''
    review_commands = ReviewCommand.query.order_by(ReviewCommand.executed_at.desc()).all()

    log = []
    for command in review_commands:
        review = command.review  # Assuming the relationship to Review is set correctly
        log_entry = {
            "Command ID": command.id,
            "Command Type": command.command_type,
            "Review ID": command.review_id,
            "Executed At": command.executed_at.strftime('%Y-%m-%d %H:%M:%S'),
            "Review Details": review.details if review else "N/A",
        }
        log.append(log_entry)

    return log
