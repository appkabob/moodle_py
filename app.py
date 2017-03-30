import constants
from models.moodle_utils import Moodle
from models.course import Course
from resources.report import ApplicationDisseminationReport, CourseEvaluationReport
from models.user import User
from models.email import BCYouShouldLiveChatEmail

# email = BCYouShouldLiveChatEmail('nick.alexander@cecillinois.org')

users = User.get_users_enrolled(4)
course = Course(name='BeyondCompliancePart3', courseid=constants.COURSE_IDS['beyond_compliance'])
groups = course.fetch_groups()
demo_group = [group for group in groups if group.name == 'Demo'][0]
demo_group.fetch_userids()

userids_to_exclude = [22, 24, 25, 38]  # 154 test admin accounts
userids_to_exclude.extend(demo_group.userids)

users = [user for user in users if user.userid not in userids_to_exclude]

users_to_email = []
for user in users:
    # course = Course(name='Beyond Compliance Part 3', courseid=4)
    course.activities = []
    activities = course.fetch_activities_status_by_user(userid=user.userid)

    if activities:
        for activity in activities:
            if activity.status['cmid'] == 46 and activity.status['state'] == 0:
                users_to_email.append(user)
                break

print('USERS TO EMAIL:')
print(users_to_email)

proceed = input('Proceed? ')
if proceed == 'y':
    for user in users_to_email:
        BCYouShouldLiveChatEmail(user, 'March 30 at 1 pm').send()




# # users = User.get_users_for_course(4)
# users = User.get_users_enrolled(4)
#
# for user in users:
#     # if user.userid == 36 or user.userid == 35:
#     course = Course(name='Beyond Compliance Part 3', scoid=12, userid=user.userid)
#     interactions = course.fetch_interactions_by_user(user.userid)
#     if interactions and user.userid != 6:
#         print(user)
#         ce_report = CourseEvaluationReport(course, user)
#         ce_report.save_pdf()
#         ad_report = ApplicationDisseminationReport(course, user)
#         ad_report.save_pdf()
#         # break
