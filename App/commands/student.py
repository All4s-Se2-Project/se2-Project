from App.models.student import Student
from App.database import db
from App.commands.command import Command


class CreateStudentCommand(Command):
    def __init__(self, username, UniId, firstname, lastname, email, password,
                 faculty, admittedTerm, degree, gpa):
        self.username = username
        self.UniId = UniId
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.faculty = faculty
        self.admittedTerm = admittedTerm
        self.degree = degree
        self.gpa = gpa

    def execute(self):
        new_student = Student(
            username=self.username,
            UniId=self.UniId,
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email,
            password=self.password,
            faculty=self.faculty,
            admittedTerm=self.admittedTerm,
            degree=self.degree,
            gpa=self.gpa,
        )
        db.session.add(new_student)
        try:
            db.session.commit()
            return new_student
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create student: {str(e)}")


class GetStudentByIdCommand(Command):
    def __init__(self, student_id):
        self.student_id = student_id

    def execute(self):
        student = Student.query.filter_by(ID=self.student_id).first()
        if not student:
            raise ValueError(f"Student with ID {self.student_id} not found")
        return student


class UpdateStudentFromTranscriptCommand(Command):
    def __init__(self, student_id, transcript_data):
        self.student_id = student_id
        self.transcript_data = transcript_data

    def execute(self):
        student = Student.query.filter_by(ID=self.student_id).first()
        if not student:
            raise ValueError(f"Student with ID {self.student_id} not found")

        student.UniId = self.transcript_data.get("id", student.UniId)
        student.gpa = self.transcript_data.get("gpa", student.gpa)
        student.faculty = self.transcript_data.get("faculty", student.faculty)
        student.degree = self.transcript_data.get("programme", student.degree)
        student.admittedTerm = self.transcript_data.get("admittedTerm", student.admittedTerm)

        try:
            db.session.commit()
            return student
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to update student from transcript: {str(e)}")
