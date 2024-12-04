import click, pytest, sys
import nltk
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from App.controllers.rating import calculateKarma
from App.controllers.staff import student_search, delete_review, add_rating, create_review



from App.controllers.rating import RatingController, calculateKarma
from App.controllers.review import ReviewController
from App.controllers.reviewCommand import ReviewCommandController
from App.controllers.user import get_history_by_date, get_history_by_range, get_latest_version
from App.database import db, get_migrate
from App.main import create_app
from App.models import Student, Karma
from App.controllers import (
    create_student, create_staff, create_admin, get_all_users_json,
    get_all_users, get_transcript, get_student_by_UniId, setup_nltk,
    analyze_sentiment, get_total_As, get_total_courses_attempted,
    calculate_academic_score, create_incident_report,
    create_accomplishment, get_staff_by_id, get_student_by_id,
    create_job_recommendation, create_karma, get_karma, get_all_history, rating)

from flask.cli import AppGroup
from App.controllers.user import (
    create_user,
    get_user,
    get_all_users,
    update_user_username,
)


'''push, pop,'''
'''create_review,'''
from App.controllers.review import ReviewController

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)



@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()

  create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 UniId='816031160',
                 degree="")

  create_student(username="shivum",
                 UniId='816016480',
                 firstname="Shivum",
                 lastname="Praboocharan",
                 email="shivum.praboocharan@my.uwi.edu",
                 password="shivumpass",
                 faculty="FST",
                 degree="Bachelor of Computer Science with Management")

  create_student(username="jovani",
                 UniId='816026834',
                 firstname="Jovani",
                 lastname="Highley",
                 email="jovani.highley@my.uwi.edu",
                 password="jovanipass",
                 faculty="FST",
                 degree="Bachelor of Computer Science with Management")

  create_student(username="kasim",
                 UniId='816030847',
                 firstname="Kasim",
                 lastname="Taylor",
                 email="kasim.taylor@my.uwi.edu",
                 password="kasimpass",
                 faculty="FST",
                 degree="Bachelor of Computer Science (General")

  create_student(username="brian",
                 UniId='816031609',
                 firstname="Brian",
                 lastname="Cheruiyot",
                 email="brian.cheruiyot@my.uwi.edu",
                 password="brianpass",
                 faculty="FST",
                 degree="Bachelor of Computer Science (General)")
  
  #Creating staff
  create_staff(username="tim",
               firstname="Tim",
               lastname="Long",
               email="",
               password="timpass",
               faculty="")

  create_staff(username="vijay",
               firstname="Vijayanandh",
               lastname="Rajamanickam",
               email="Vijayanandh.Rajamanickam@sta.uwi.edu",
               password="vijaypass",
               faculty="FST")

  create_staff(username="permanand",
               firstname="Permanand",
               lastname="Mohan",
               email="Permanand.Mohan@sta.uwi.edu",
               password="password",
               faculty="FST")

  create_job_recommendation(
      2, 7, False, "Job", "1",
      "I am seeking a recommnedation for a position at a company", "WebTech",
      "Web Developer", "webtech@gmail.com")
  create_job_recommendation(
      2, 8, False, "Job", "1",
      "I am seeking a recommnedation for a position at a company", "WebTech",
      "Web Developer", "webtech@gmail.com")
  create_accomplishment(2, False, "Permanand Mohan", "Runtime",
                        "I placed first at runtime.", 0, "None Yet")
  create_accomplishment(2, False, "Vijayanandh Rajamanickam", "Runtime",
                        "I placed first at runtime.", 0, "None Yet")
  
  staff = get_staff_by_id(7)
  student1 = get_student_by_UniId(816031609)
  ReviewController.create_review(staff, student1, True, 5, 50, "Behaves very well in class!")

  student2 = get_student_by_UniId(816016480)
  ReviewController.create_review(staff, student2, True, 5,50, "Behaves very well in class!")
  student3 = get_student_by_UniId(816026834)
  ReviewController.create_review(staff, student3, True, 5, 50, "Behaves very well in class!")
  student4 = get_student_by_UniId(816030847)
  ReviewController.create_review(staff, student4, True, 5, 50,  "Behaves very well in class!")
  
  create_admin(username="admin",
               firstname="Admin",
               lastname="Admin",
               email="admin@example.com",
               password="password",
               faculty="FST")

  students = Student.query.all()

  for student in students:
    
    if student:
      print(student.id)
      create_karma(student.id)
      student.karmaID = get_karma(student.id).karmaID
      print(get_karma(student.id).karmaID)
      db.session.commit()


@app.cli.command("nltk_test", help="Tests nltk")
@click.argument("sentence", default="all")
def analyze(sentence):
  analyze_sentiment(sentence)
  return


# '''
# User Commands
# '''

# # Commands can be organized using groups

# # create a group, it would be the first argument of the comand
# # eg : flask user <command>
# # user_cli = AppGroup('user', help='User object commands')

# # # Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(id, username, firstname,lastname , password, email, faculty):
#     create_user(id, username, firstname,lastname , password, email, faculty)
#     print(f'{username} created!')

# # this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

# app.cli.add_command(user_cli) # add the group to the cli
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')

@test.command("final", help="Runs ALL tests")
@click.argument("type", default="all")
def final_tests_command(type):
  if type == "all":
    sys.exit(pytest.main(["App/tests"]))

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "UserUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "StudentUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def staff_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "StaffUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("review", help="Run Review tests")
@click.argument("type", default="all")
def review_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("recommendation", help="Run Recommendation tests")
@click.argument("type", default="all")
def recommendation_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "RecommendationUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "RecommendationIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("karma", help="Run Karma tests")
@click.argument("type", default="all")
def karma_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "KarmaUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "KarmaIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("incidentreport", help="Run Incident Report tests")
@click.argument("type", default="all")
def incident_reports_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "IncidentReportUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "IncidentReportIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("accomplishment", help="Run Accomplishment tests")
@click.argument("type", default="all")
def accomplishment_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "AccomplishmentUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "AccomplishmentIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("grades", help="Run Grades tests")
@click.argument("type", default="all")
def grades_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "GradesUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "GradesIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("admin", help="Run Admin tests")
@click.argument("type", default="all")
def admin_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "AdminUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("nltk", help="Run NLTK tests")
@click.argument("type", default="all")
def nltk_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "NLTKUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "NLTKIntegrationTests"]))


@test.command("print", help="print get_transcript")
@click.argument("type", default="all")
def print_transcript(type):
  studentID = input("Enter student ID: ")  
  transcripts = get_transcript(
      studentID)  # Get transcript data for the student
  if transcripts:
    for transcript in transcripts:
      if type == "all":
        print(transcript.to_json())  # Print all transcript data as JSON
      # elif type == "id":
      #     print(transcript.studentID)  # Print student ID
      # elif type == "gpa":
      #     print(transcript.gpa)  # Print GPA
      # elif type == "fullname":
      #     print(transcript.fullname)  # Print full name
      # Add more options as needed
      else:
        print(
            "Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options."
        )
  else:
    print("Transcript not found for student with ID:", studentID)


@test.command("printstu", help="print get_student")
@click.argument("type", default="all")
def print_student(type):
  UniId = input("Enter student ID: ")
  student = get_student_by_UniId(UniId)
  if student:
    if type == "all":
      print(student.to_json(0))
    # elif type == "id":
    #     print(student.UniId)
    # elif type == "gpa":
    #     print(student.gpa)
    # elif type == "fullname":
    #     print(student.fullname)
    else:
      print(
          "Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options."
      )
  else:
    print("Student not found with ID:", UniId)


@test.command("printgradepointsandgpa_weight",
              help="print student grade points from transcript")
@click.argument("type", default="all")
def print_grade_points(type):
  UniId = input("Enter student ID: ")
  points = get_total_As(UniId)
  cources_attempted = get_total_courses_attempted(UniId)
  if points:
    print('points ', points)
    print('courses attepmtped:, ', cources_attempted)

  else:
    print("Student not found with ID:", UniId)


@test.command("printacademicscore", help="print student academic weight")
@click.argument("type", default="all")
def print_academic_weight(type):
  UniId = input("Enter student ID: ")
  points = get_total_As(UniId)
  cources_attempted = get_total_courses_attempted(UniId)
  academic_score = calculate_academic_score(UniId)
  if points:
    print('points ', points)
    print('courses attepmtped:, ', cources_attempted)
    print('Academic Score:, ', academic_score)

  else:
    print("Student not found with ID:", UniId)


app.cli.add_command(test)


'''
History Commands
'''

history_cli = AppGroup('history', help='Commands for managing review command history')

'''
@history_cli.command("push", help="Push a reviewCommand ID into the history")
@click.argument("review_command_id", type=int)
def push_command(review_command_id):
    try:
        entry = push(review_command_id)
        click.echo(f"History pushed: ID={entry.reviewCommand_id}, Timestamp={entry.timestamp}")
    except Exception as e:
        click.echo(f"Failed to push history: {e}")
'''
'''
@history_cli.command("pop", help="Pop the most recent reviewCommand ID from the history")
@click.argument("review_command_id", type=int)
def pop_command(review_command_id):
    try:
        entry = pop(review_command_id)
        if entry:
            click.echo(f"History popped: ID={entry.reviewCommand_id}, Timestamp={entry.timestamp}")
        else:
            click.echo(f"No history found for reviewCommand ID {review_command_id}")
    except Exception as e:
        click.echo(f"Failed to pop history: {e}")

app.cli.add_command(history_cli)
'''
'''
User Commands
'''

user_history_cli = AppGroup('user_history', help='Commands for managing user history')

@user_history_cli.command("all_history", help="Get all history entries for a user")
@click.argument("user_id", type=int)
def get_all_history_command(user_id):
    try:
        history = get_all_history(user_id)
        if 'error' in history:
            click.echo(f"Error: {history['error']}")
        else:
            if not history:
                click.echo(f"No history found for user ID {user_id}.")
            else:
                for entry in history:
                    click.echo(f"ID: {entry['id']}, ReviewCommand ID: {entry['reviewCommand_id']}, Timestamp: {entry['timestamp']}")
    except Exception as e:
        click.echo(f"Error fetching history: {e}")

@user_history_cli.command("by_date", help="Get user history entries filtered by date")
@click.argument("user_id", type=int)
@click.argument("date", type=str)
def get_history_by_date_command(user_id, date):
    
    try:
        history = get_history_by_date(user_id, date)
        if 'error' in history:
            click.echo(f"Error: {history['error']}")
        else:
            if not history:
                click.echo(f"No history found for user ID {user_id} on date {date}.")
            else:
                for entry in history:
                    click.echo(f"ID: {entry['id']}, ReviewCommand ID: {entry['reviewCommand_id']}, Timestamp: {entry['timestamp']}")
    except Exception as e:
        click.echo(f"Error fetching history by date: {e}")

@user_history_cli.command("by_range", help="Get user history entries within a date range")
@click.argument("user_id", type=int)
@click.argument("start_date", type=str)
@click.argument("end_date", type=str)
def get_history_by_range_command(user_id, start_date, end_date):

    try:
        history = get_history_by_range(user_id, start_date, end_date)
        if 'error' in history:
            click.echo(f"Error: {history['error']}")
        else:
            if not history:
                click.echo(f"No history found for user ID {user_id} in the range {start_date} to {end_date}.")
            else:
                for entry in history:
                    click.echo(f"ID: {entry['id']}, ReviewCommand ID: {entry['reviewCommand_id']}, Timestamp: {entry['timestamp']}")
    except Exception as e:
        click.echo(f"Error fetching history by range: {e}")

@user_history_cli.command("latest_version", help="Get the latest history entry for a user")
@click.argument("user_id", type=int)
def get_latest_version_command(user_id):
    """Get the latest history entry for a specific user."""
    try:
        latest = get_latest_version(user_id)
        if 'error' in latest:
            click.echo(f"Error: {latest['error']}")
        elif 'message' in latest:
            click.echo(latest['message'])
        else:
            click.echo(f"ID: {latest['id']}, ReviewCommand ID: {latest['reviewCommand_id']}, Timestamp: {latest['timestamp']}")
    except Exception as e:
        click.echo(f"Error fetching latest history entry: {e}")

app.cli.add_command(user_history_cli)

@app.cli.command('display_review')
@click.argument('review_id')
def display_review_cli(review_id):
    
    controller = ReviewController()  
    result = controller.display_review(review_id) 

    if result:
        print(f"Review displayed successfully: {result}")
    else:
        print("Failed to display review.")

#testing this command        
@app.cli.command('get_all_student_reviews', help="Get the review log of a user")
@click.argument('student_id', type=int, default=1)
def get_all_student_reviews_cli(student_id):
    stud = Student.query.get(student_id)
    if stud:
        print(f'Review log for Student ID {student_id}:')
        for review in stud.reviews:
          print(f'Review {review.id} was created by {review.reviewing_staff.first_name} {review.reviewing_staff.last_name} on {review.date_created}')    
    else:
        print("Student not found.")

@app.cli.command("review_at_time", help="Get review for a user at a specific time")
@click.argument("student_id", type=int, default=1)
@click.argument("time", type=str, default="1 min ago")  # Assume time is given in ISO format e.g., "2023-01-15T12:00:00"
def get_review_at_time(student_id, time):
    from datetime import datetime
    from datetime import timedelta
    stud = Student.query.get(student_id)
    if stud:
        if time=="1 min ago":
            review_at_time = stud.get_review_at_time(datetime.utcnow() - timedelta(minutes=1))
        else:
            review_at_time = stud.get_review_at_time(datetime.fromisoformat(time))
        
        if review_at_time:
            print(f"Review for Student {student_id} at {time}:")
            print(review_at_time)
        else:
            print(f"No review found for Student {student_id} at {time}.")
    else:
        print('Student not found.')

@app.cli.command('calculate_karma', help='Calculate karma for a student based on a review')
@click.argument('review_id', type=int)
@click.argument('star_rating', type=int)
def calculate_karma_cli(review_id, star_rating):
   
    print(f"Calculating karma for Review ID: {review_id} with Star Rating: {star_rating}")
    try:
        new_karma = calculateKarma(review_id, star_rating)  
        if new_karma is not None:
            print(f"Karma updated successfully. New Karma: {new_karma}")
        else:
            print("Failed to calculate karma.")
    except Exception as e:
        print(f"Error during karma calculation: {e}")



'''
Rating Commands
'''

rating_cli = AppGroup('rating', help='Commands for managing ratings')


@rating_cli.command("execute", help="Execute a pending rating command")
def execute_rating_command():
  
    controller = RatingController()  
    result = controller.execute()  
    if result:
        print(f"Rating command executed successfully. ID: {result.id}, Review ID: {result.review_id}")
    else:
        print("Failed to execute rating command or no pending command found.")


@rating_cli.command("log_change", help="Log changes for a rating command")
def log_change_rating_command():
    controller = RatingController()  
    result = controller.logChange()  
    if result:
        print(f"Changes logged successfully for RatingCommand ID: {result.id}")
    else:
        print("Failed to log changes or no executed command found.")


@rating_cli.command("calculate_karma", help="Calculate karma for a student based on review and star rating")
@click.argument("review_id", type=int)
@click.argument("star_rating", type=int)
def calculate_karma_cli(review_id, star_rating):
   
    print(f"Calculating karma for Review ID: {review_id} with Star Rating: {star_rating}")
    new_karma = calculateKarma(review_id, star_rating)  

    if new_karma is not None:
        print(f"Karma updated successfully. New Karma: {new_karma}")
    else:
        print("Failed to update karma.")



app.cli.add_command(rating_cli)

'''
Review Command CLI Commands
'''

review_command_cli = AppGroup('review_command', help='Commands for managing review commands')


@review_command_cli.command("execute", help="Execute the most recent review command")
def execute_review_command():
    
    controller = ReviewCommandController() 
    result = controller.execute()  
    if result:
        print(f"ReviewCommand executed successfully. ID: {result.id}")
    else:
        print("Failed to execute review command or no command found.")


@review_command_cli.command("log_change", help="Log changes for the most recent review command")
def log_change_review_command():
   
    controller = ReviewCommandController()  
    result = controller.logChange() 
    if result:
        print(f"Changes logged successfully for ReviewCommand ID: {result.id}")
    else:
        print("Failed to log changes or no command found.")

app.cli.add_command(review_command_cli)

'''
Staff CLI Commands
'''

staff_cli = AppGroup('staff', help='Commands for staff operations')

@staff_cli.command("student_search", help="Search for a student")
@click.argument("student_id")
def cli_student_search(student_id):
    try:
        student = student_search(student_id)
        if student:
            print(f"Student found: {student.to_json()}")
        else:
            print(f"No student found with ID: {student_id}")
    except Exception as e:
        print(f"Error: {e}")

@staff_cli.command("delete_review", help="Delete a review by ID")
@click.argument("review_id", type=int)
def cli_delete_review(review_id):
    try:
        success = delete_review(review_id)
        if success:
            print(f"Review with ID {review_id} deleted successfully.")
        else:
            print(f"Failed to delete review with ID {review_id}.")
    except Exception as e:
        print(f"Error: {e}")

@staff_cli.command("add_rating", help="Add a rating to a review")
@click.argument("review_id", type=int)
@click.argument("rating_value", type=int)
def cli_add_rating(review_id, rating_value):
    try:
        success = add_rating(review_id, rating_value)
        if success:
            print(f"Rating added to review {review_id} successfully.")
        else:
            print(f"Failed to add rating to review {review_id}.")
    except Exception as e:
        print(f"Error: {e}")

@staff_cli.command("create_review")
@click.argument("staff_id", type=int)
@click.argument("is_positive", type=bool)
@click.argument("student_id", type=int)
@click.argument("rating", type=int)
@click.argument("points", type=int)
@click.argument("details", type=str)
def cli_create_review(staff_id, is_positive, student_id, rating, points, details):
    from App.controllers import create_review
    try:
        review = create_review(staff_id, is_positive, student_id, rating, points, details)
        print(f"Review created successfully: {review.to_json()}")
    except ValueError as e:
        print(f"Error: {e}")



app.cli.add_command(staff_cli)

student_cli = AppGroup('student', help='Commands for managing students')

@student_cli.command("display_karma", help="Display karma score for a specific student")
@click.argument("student_id", type=int)
def display_karma(student_id):
    student = get_student_by_id(student_id)
    if not student:
        print(f"Student with ID {student_id} not found.")
        return

    try:
        print(student.displayKarma())
    except AttributeError as e:
        print(f"Error: {str(e)} - Ensure the student model includes a 'karma' field and the 'displayKarma' method.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


app.cli.add_command(student_cli)




if __name__ == "__main__":
    app.run()