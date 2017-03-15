from models.interaction import Interaction
from models.moodle_utils import Moodle


class Course:
    def __init__(self, name, scoid, userid, status=None, max_score=None, min_score=None, raw_score=None, total_time=None):
        self.name = name
        self.scoid = scoid
        self.userid = userid
        self.status = status
        self.max_score = max_score
        self.min_score = min_score
        self.raw_score = raw_score
        self.total_time = total_time

        self.interactions = []

    def __repr__(self):
        return '<Course {} {}>'.format(self.scoid, self.name)

    def fetch_interactions(self):
        payload = 'scoid={}&userid={}'.format(self.scoid, self.userid)
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