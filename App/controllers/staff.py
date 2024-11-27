from App.commands.staff import (
    CreateStaffCommand,
    GetStaffByIdCommand,
    EditStaffReviewCommand,
    CreateStaffReviewCommand,
    GetStaffByUsernameCommand,
    GetStaffByNameCommand,
)


class StaffController:
    def create_staff(self, username, firstname, lastname, email, password, faculty):
        try:
            command = CreateStaffCommand(username, firstname, lastname, email, password, faculty)
            return command.execute()
        except ValueError as e:
            print(f"[StaffController.create_staff] Error: {str(e)}")
            return None

    def get_staff_by_id(self, staff_id):
        try:
            command = GetStaffByIdCommand(staff_id)
            return command.execute()
        except ValueError as e:
            print(f"[StaffController.get_staff_by_id] Error: {str(e)}")
            return None

    def get_staff_by_username(self, username):
        try:
            command = GetStaffByUsernameCommand(username)
            return command.execute()
        except ValueError as e:
            print(f"[StaffController.get_staff_by_username] Error: {str(e)}")
            return None

    def get_staff_by_name(self, firstname, lastname):
        try:
            command = GetStaffByNameCommand(firstname, lastname)
            return command.execute()
        except ValueError as e:
            print(f"[StaffController.get_staff_by_name] Error: {str(e)}")
            return None

    def staff_edit_review(self, review_id, details):
        try:
            command = EditStaffReviewCommand(review_id, details)
            return command.execute()
        except ValueError as e:
            print(f"[StaffController.staff_edit_review] Error: {str(e)}")
            return None

    def staff_create_review(self, staff_id, student_id, is_positive, points, details):
        try:
            command = CreateStaffReviewCommand(staff_id, student_id, is_positive, points, details)
            return command.execute()
        except ValueError as e:
            print(f"[StaffController.staff_create_review] Error: {str(e)}")
            return None
