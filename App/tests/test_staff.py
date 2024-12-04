import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Staff
from App.controllers import (
    create_staff, 
    get_staff_by_id,
    get_staff_by_name,
    get_staff_by_username,
    create_student,
    get_student_by_username,
    get_student_by_UniId,
    delete_review, 
    student_search, 
    add_rating, 
    create_review,
    get_review,
    get_reviewID
)
'''
   Unit Tests
'''
class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
        staff = Staff(username="joe",first_name="Joe", last_name="Mama", email="joe@example.com", password="joepass", faculty="FST")
        assert staff.username == "joe"

    def test_get_json(self):
        staff = Staff(username="joe",first_name="Joe", last_name="Mama", email="joe@example.com", password="joepass", faculty="FST")
        staff_json = staff.to_json()
        print(staff_json)
        self.assertDictEqual(staff_json, {"staffID": None,
            "username": "joe",
            "first_name": "Joe",
            "last_name": "Mama",
            "email": "joe@example.com",
            "faculty": "FST",
            "reviews": []})


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

class StaffIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        assert create_staff(username="testuser", firstname="Test", lastname="User", email="test1@example.com", password="testpass", faculty="FST") == True
    
    def test_get_staff_by_id(self):
        staff = get_staff_by_id(1)
        assert staff is not None

    def test_get_staff_by_name(self):
        staff = get_staff_by_name("Test", "User")
        assert staff is not None
    
    def test_get_staff_by_username(self):
        staff = get_staff_by_username("testuser")
        assert staff is not None

    def test_student_search(self):
        assert create_student(username="student1", UniId="816000000", firstname="Student", lastname="One", email="student1@example.com", password="studentpass", faculty="FST", degree="CS") == True
        student = get_student_by_username("student1")
        assert student is not None
        staff = get_staff_by_id(1)
        assert staff is not None
        found_student = student_search("student1", "816000000", "FST", "CS")
        assert found_student is not None
        assert found_student.username == "student1"
        assert found_student.UniId == "816000000"
        assert found_student.faculty == "FST"
        assert found_student.degree == "CS"