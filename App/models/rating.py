from App.database import db

class RatingCommand(db.Model):
  __tablename__ = 'rating_command' 
  id = db.Column(db.Integer, primary_key=True) 
  review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False) 
  rating_value = db.Column(db.Integer, nullable=False)

  def __init__(self, review_id: int, rating_value: int): 
    self.review_id = review_id 
    self.rating_value = rating_value 
    
  def __repr__(self): 
    return f"<Rating: {self.rating_value} for Review {self.review_id}>"
