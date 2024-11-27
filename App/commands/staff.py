from App.models.staff import Staff
from App.models.review import Review
from App.database import db
from App.commands.command import Command


class CreateStaffCommand(Command):
    def __init__(self, username, firstname, lastname, email, password, faculty):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.faculty = faculty

    def execute(self):
        new_staff = Staff(
            username=self.username,
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email,
            password=self.password,
            faculty=self.faculty,
        )
        db.session.add(new_staff)
        try:
            db.session.commit()
            return new_staff
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create staff: {str(e)}")


class GetStaffByIdCommand(Command):
    def __init__(self, staff_id):
        self.staff_id = staff_id

    def execute(self):
        staff = Staff.query.filter_by(ID=self.staff_id).first()
        if not staff:
            raise ValueError(f"Staff with ID {self.staff_id} not found")
        return staff


class GetStaffByUsernameCommand(Command):
    def __init__(self, username):
        self.username = username

    def execute(self):
        staff = Staff.query.filter_by(username=self.username).first()
        if not staff:
            raise ValueError(f"Staff with username {self.username} not found")
        return staff


class GetStaffByNameCommand(Command):
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def execute(self):
        staff = Staff.query.filter_by(firstname=self.firstname, lastname=self.lastname).first()
        if not staff:
            raise ValueError(f"Staff {self.firstname} {self.lastname} not found")
        return staff


class EditStaffReviewCommand(Command):
    def __init__(self, review_id, details):
        self.review_id = review_id
        self.details = details

    def execute(self):
        review = Review.query.filter_by(ID=self.review_id).first()
        if not review:
            raise ValueError(f"Review with ID {self.review_id} not found")

        review.details = self.details
        try:
            db.session.commit()
            return review
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to edit review: {str(e)}")


class CreateStaffReviewCommand(Command):
    def __init__(self, staff_id, student_id, is_positive, points, details):
        self.staff_id = staff_id
        self.student_id = student_id
        self.is_positive = is_positive
        self.points = points
        self.details = details

    def execute(self):
        new_review = Review(
            staff_id=self.staff_id,
            student_id=self.student_id,
            is_positive=self.is_positive,
            points=self.points,
            details=self.details,
        )
        db.session.add(new_review)
        try:
            db.session.commit()
            return new_review
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create review: {str(e)}")
