import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Student
from App.controllers import (
    create_student,
    displayKarma,
    get_student_by_id,
    get_student_by_UniId,
    get_student_by_username,
    get_students_by_degree,
    get_students_by_faculty,
    get_all_students_json,
    update_degree,
    get_review_at_time
)

'''
   Unit Tests
'''
class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        student = Student(username="billy", 
                          UniId="816000000", 
                          first_name="Billy", 
                          last_name="John", 
                          email="billy@example.com", 
                          password="billypass", 
                          faculty="FST", 
                          degree="BSc Computer Science", 
                          karma = 50)
        assert student.username == "billy"

    def test_get_json(self):
        student = Student(username="billy", 
                          UniId="816000000", 
                          first_name="Billy", 
                          last_name="John", 
                          email="billy@example.com", 
                          password="billypass", 
                          faculty="FST", 
                          degree="BSc Computer Science", 
                          karma=50)
        student_json = student.to_json()
        print(student_json)
        self.assertDictEqual(student_json, {"studentID": None,
            "username": "billy",
            "fullName": "Billy John",
            "degree": "BSc Computer Science",
            "uniId": "816000000",
            "karma": 50})


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

class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        assert create_student(username="billy",
                              UniId="816000000", 
                              firstname="Billy", 
                              lastname="John",
                              email="billy@example.com", 
                              password="billypass", 
                              faculty="FST",
                              degree="BSc Computer Science") == True
        
    def test_get_student_by_id(self):
        student = get_student_by_id(1)
        assert student is not None
    
    def test_get_student_by_username(self):
        student = get_student_by_username("billy")
        assert student is not None

    def test_get_students_by_degree(self):
        students = get_students_by_degree("BSc Computer Science")
        assert students != []

    def test_get_students_by_faulty(self):
        students = get_students_by_faculty("FST")
        assert students != []
    
    def test_get_students_json(self):
        students = get_all_students_json()
        assert students != []
    
    def test_get_student_by_UniId(self):
      student = get_student_by_UniId("816000000")
      assert student is not None
    
    def test_update_degree(self):
        assert update_degree(1, "BSc Computer Science Special") == True

    def test_display_karma(self):
        assert displayKarma(1) == "Karma Points for Student Billy John (ID: 1): 50"

    '''def test_get_review_at_time(self):
        review_data = get_review_at_time(self.date_created)
        expected_data = {
            "reviewID": self.review.id,
            "reviewer": f"{self.staff.first_name} {self.staff.last_name}",
            "studentID": self.student.id,
            "studentName": f"{self.student.first_name} {self.student.last_name}",
            "created": self.date_created.strftime("%d-%m-%Y %H:%M"),
            "points": self.review.points,
            "details": self.review.details,
            "rating": self.review.rating,
        }
        self.assertEqual(review_data, expected_data)'''