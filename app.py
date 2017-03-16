from models.moodle_utils import Moodle
from models.course import Course
from resources.report import ApplicationDisseminationReport, CourseEvaluationReport
from models.user import User

# users = User.get_users_for_course(4)
users = User.get_users_enrolled(4)

for user in users:
    # if user.userid == 36 or user.userid == 35:
    course = Course('Beyond Compliance Part 3', 12, user.userid)
    interactions = course.fetch_interactions()
    if interactions and user.userid != 6:
        print(user)
        ce_report = CourseEvaluationReport(course, user)
        ce_report.save_pdf()
        ad_report = ApplicationDisseminationReport(course, user)
        ad_report.save_pdf()
        # break
