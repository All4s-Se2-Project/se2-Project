from App.models import Review
from App.database import db

# Display review by ID (mapping to displayReview from the diagram)
def display_review(review_id):
    review = Review.query.get(review_id)
    if review:
        return review.to_json()
    return {"error": "Review not found"}
