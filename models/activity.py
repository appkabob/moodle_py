from models.interaction import Interaction
from models.moodle_utils import Moodle


class Activity:
    def __init__(self, cmid, userid, status=None):
        self.cmid = cmid
        self.userid = userid
        self.status = status
        self.interactions = []

    def __repr__(self):
        return "<Activity cmid {} state {}>".format(self.status['cmid'], self.status['state'])

    def fetch_interactions_by_user(self):
        payload = 'scoid={}&userid={}'.format(self.cmid, self.userid)
        interactions = Moodle().submit_request('mod_scorm_get_scorm_sco_tracks', payload)
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