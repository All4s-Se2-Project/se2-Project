from App.models import ReviewCommandHistory, db
from datetime import datetime

def push(reviewCommand_id: int):
    try:
        history_entry = ReviewCommandHistory(reviewCommand_id=reviewCommand_id)
        db.session.add(history_entry)
        db.session.commit()
        return history_entry
    except Exception as e:
        db.session.rollback()
        print(f"Error pushing history: {e}")
        raise

def pop(reviewCommand_id: int):
    try:
        history_entry = (
            ReviewCommandHistory.query
            .filter_by(reviewCommand_id=reviewCommand_id)
            .order_by(ReviewCommandHistory.timestamp.desc())
            .first()
        )

        if not history_entry:
            print(f"No history found for reviewCommand_id {reviewCommand_id}")
            return None

        db.session.delete(history_entry)
        db.session.commit()
        return history_entry
    except Exception as e:
        db.session.rollback()
        print(f"Error popping history: {e}")
        raise
