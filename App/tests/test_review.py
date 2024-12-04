import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Review
from App.controllers import (
    create_student,
    create_staff,
    get_staff_by_username,
    get_staff_by_id,
    get_student_by_id,
    get_student_by_username,
    create_review,
    delete_review,
    get_review
)

from App.controllers.review import ReviewController

'''
   Unit Tests
'''
class ReviewUnitTests(unittest.TestCase):

    def test_new_review(self):
        assert create_staff(username="joe",
                            firstname="Joe", 
                            lastname="Mama", 
                            email="joe@example.com", 
                            password="joepass", 
                            faculty="FST") == True
        assert create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 UniId='816031160',
                 degree="CS") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        review = Review(staff, student, True, 3, 3, "Billy is good.")
        assert review is not None

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class ReviewIntegrationTests(unittest.TestCase):

    def test_display_review(self):
        assert create_staff(username="joe2",
                            firstname="Joe2", 
                            lastname="Mama2", 
                            email="joe2@example.com", 
                            password="joepass2", 
                            faculty="FST") == True
        assert create_student(username="billy2",
                 firstname="Billy2",
                 lastname="John2",
                 email="billy2@example.com",
                 password="billypass2",
                 faculty="FST",
                 UniId='816031162',
                 degree="CS") == True
        student = get_student_by_username("billy2")
        staff = get_staff_by_username("joe2")
        review = create_review(staff.id, True, student.UniId, 5, "Billy is good.")
        assert review is not None
        review_id = review.id
        assert ReviewController().display_review(review_id) is not None