from App.commands.student import (
    CreateStudentCommand,
    GetStudentByIdCommand,
    UpdateStudentFromTranscriptCommand,
)


class StudentController:
    def create_student(self, username, UniId, firstname, lastname, email, password,
                       faculty, admittedTerm, degree, gpa):
        try:
            command = CreateStudentCommand(
                username, UniId, firstname, lastname, email, password, faculty, admittedTerm, degree, gpa
            )
            return command.execute()
        except ValueError as e:
            print(f"[StudentController.create_student] Error: {str(e)}")
            return None

    def get_student_by_id(self, student_id):
        try:
            command = GetStudentByIdCommand(student_id)
            return command.execute()
        except ValueError as e:
            print(f"[StudentController.get_student_by_id] Error: {str(e)}")
            return None

    def update_student_from_transcript(self, student_id, transcript_data):
        try:
            command = UpdateStudentFromTranscriptCommand(student_id, transcript_data)
            return command.execute()
        except ValueError as e:
            print(f"[StudentController.update_student_from_transcript] Error: {str(e)}")
            return None
