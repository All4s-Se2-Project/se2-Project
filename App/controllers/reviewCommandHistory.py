from App.database import db
from datetime import datetime
from App.models import ReviewCommandHistory 

def push_review_history():
  data = request.get_json()
  if not data or 'reviewCommand_id' not in data:
          return jsonify({'error': 'reviewCommand_id is required'}), 400
  
      try:
          reviewCommand_id = data['reviewCommand_id']
          new_history = ReviewCommandHistory(reviewCommand_id=reviewCommand_id)
  
          db.session.add(new_history)
          db.session.commit()
  
          return jsonify({
              'message': 'ReviewCommand history added successfully',
              'reviewCommand_id': new_history.reviewCommand_id,
              'timestamp': new_history.timestamp
          }), 201
  
      except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def pop_review_history(reviewCommand_id):
    try:
        latest_history = ReviewCommandHistory.query.filter_by(reviewCommand_id=reviewCommand_id).order_by(ReviewCommandHistory.timestamp.desc()).first()

        if not latest_history:
            return jsonify({'error': 'No history found for the given reviewCommand_id'}), 404

        db.session.delete(latest_history)
        db.session.commit()

        return jsonify({
            'message': 'Latest ReviewCommand history deleted successfully',
            'reviewCommand_id': latest_history.reviewCommand_id,
            'timestamp': latest_history.timestamp
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
