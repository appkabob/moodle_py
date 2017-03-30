import constants
from models.activity import Activity
from models.group import Group
from models.interaction import Interaction
from models.moodle_utils import Moodle


class Course:
    def __init__(self, name=None, userid=None, scoid=None, courseid=None, status=None, max_score=None, min_score=None, raw_score=None, total_time=None):
        self.name = name
        self.userid = userid
        self.scoid = scoid
        self.courseid = courseid
        self.status = status
        self.max_score = max_score
        self.min_score = min_score
        self.raw_score = raw_score
        self.total_time = total_time

        self.interactions = []
        self.activities = []
        self.groups = []

    def __repr__(self):
        return '<Course {} {}>'.format(self.scoid, self.name)

    def fetch_interactions_by_user(self, userid):
        payload = 'scoid={}&userid={}'.format(self.scoid, userid)
        interactions = Moodle().submit_request('mod_scorm_get_scorm_sco_tracks',payload)
        if interactions['warnings']:
            return None
        interactions_data = {}
        for interaction in interactions['data']['tracks']:
            if 'cmi.interactions_' in interaction['element']:
                id = interaction['element'].split('.')[1]
                field = interaction['element'].split('.')[2]

                try:
                    interactions_data[id][field] = interaction['value']
                except KeyError:
                    interactions_data[id] = {}
                    interactions_data[id][field] = interaction['value']

        # print(interactions_data)

        for key, val in interactions_data.items():
            self.interactions.append(Interaction(
                key,
                self.userid,
                val['id'],
                val['result'],
                val['student_response'],
                val['time'],
                val['type'],
                val['weighting']
            ))

        return self.interactions

    def fetch_activities_status_by_user(self, userid):
        payload = 'courseid={}&userid={}'.format(self.courseid, userid)
        activities = Moodle().submit_request('core_completion_get_activities_completion_status', payload)

        if activities['warnings']:
            return None

        for activity in activities['statuses']:
            self.activities.append(Activity(
                userid,
                activity
            ))

        return self.activities

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
