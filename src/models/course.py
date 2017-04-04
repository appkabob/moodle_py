import constants
from src.resources.report import CourseEvaluationReport, ApplicationDisseminationReport
from .activity import Activity
from .email import Email
from .group import Group
from .moodle_utils import Moodle
from .user import User


class Course:
    def __init__(self, name=None, courseid=None):  # userid=None, scoid=None, status=None, max_score=None, min_score=None, raw_score=None, total_time=None
        self.name = name
        self.courseid = courseid
        # self.userid = userid
        # self.scoid = scoid
        # self.status = status
        # self.max_score = max_score
        # self.min_score = min_score
        # self.raw_score = raw_score
        # self.total_time = total_time

        # self.interactions = []
        # self.activities = []
        self.groups = []

    def __repr__(self):
        return '<Course {} {}>'.format(self.scoid, self.name)

    def fetch_enrolled_users(self, onlyactive=False):
        payload = 'courseid={}'.format(self.courseid)
        if onlyactive:
            payload += '&options[0][name]=onlyactive&options[0][value]=1'

        users_list = Moodle().submit_request('core_enrol_get_enrolled_users', payload)
        users_objs = []
        for user in users_list:
            iein = None
            if 'customfields' in user.keys():
                for field in user['customfields']:
                    if field['shortname'] == 'iein':
                        iein = field['value']
                users_objs.append(User(
                    user['id'],
                    user['username'],
                    user['email'],
                    user['firstname'],
                    user['lastname'],
                    iein
                ))
        return users_objs

    def fetch_activities_status_by_user(self, userid):
        payload = 'courseid={}&userid={}'.format(self.courseid, userid)
        activities = Moodle().submit_request('core_completion_get_activities_completion_status', payload)

        if activities['warnings']:
            return None

        activities_objs = []
        for activity in activities['statuses']:
            activities_objs.append(Activity(
                activity['cmid'],
                userid,
                activity
            ))

        return activities_objs

    def fetch_groups(self):
        payload = 'courseid={}'.format(self.courseid)
        groups = Moodle().submit_request('core_group_get_course_groups', payload)

        # if groups['warnings']:
        #     return None

        for group in groups:
            self.groups.append(Group(
                group['id'],
                group['name']
            ))

        return self.groups


class BeyondComplianceCourse(Course):
    def __init__(self):
        self.name = 'Beyond Compliance'
        self.courseid = constants.COURSE_IDS['beyond_compliance']
        self.groups = []

    def __repr__(self):
        return "<BeyondComplianceCourse>"

    def get_enrolled_users_not_registered_for_live_chat(self):
        users = self.fetch_enrolled_users(onlyactive=True)
        groups = self.fetch_groups()
        demo_group = [group for group in groups if group.name == 'Demo'][0]

        userids_to_exclude = [22, 24, 25, 38, 154]  # test admin accounts - think about leaving one in
        userids_to_exclude.extend(demo_group.fetch_userids())

        users = [user for user in users if user.userid not in userids_to_exclude]

        users_to_email = []
        for user in users:
            activities = self.fetch_activities_status_by_user(userid=user.userid)

            if activities:
                for activity in activities:
                    if activity.status['cmid'] == constants.SCO_IDS['beyond_compliance_live_chat_registration_label'] and activity.status['state'] == 0:
                        users_to_email.append(user)
                        print(user)
                        break

        return users_to_email

    def generate_aa_reports(self):
        users = self.fetch_enrolled_users(onlyactive=False)

        for user in users:
            activity = Activity(constants.SCO_IDS['beyond_compliance_part_3'], user.userid)
            interactions = activity.fetch_interactions_by_user()
            if interactions:
                answered_last_question = [interaction.slide_id for interaction in interactions if
                                          interaction.slide_id == 'Scene1_Slide26_Essay_0_0']
                if answered_last_question and user.userid != 6:
                    print(user)
                    CourseEvaluationReport(self, user, interactions).save_pdf()
                    ApplicationDisseminationReport(self, user, interactions).save_pdf()
                    # break

    def send_email_you_should_register_for_live_chat(self, dateandtimeofnextlivechat, numberofenrollmentdays='60', to_users=[], is_test=False):
        if not to_users:
            to_users = self.get_enrolled_users_not_registered_for_live_chat()

        for to_user in to_users:
            body_template = 'src/email_templates/BCYouShouldLiveChatEmail.txt'
            with open(body_template, 'r') as f:
                read_data = f.read()
            body = read_data.\
                replace('\n', '<br />').\
                replace('{numberofenrollmentdays}', numberofenrollmentdays).\
                replace('{dateandtimeofnextlivechat}', dateandtimeofnextlivechat)

            Email(to_user, body).send(is_test)
