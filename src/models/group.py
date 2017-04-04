from .moodle_utils import Moodle


class Group:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.userids = []

    def __repr__(self):
        return "<Group {} {} - {} users>".format(self.id, self.name, len(self.userids))

    def fetch_userids(self):
        payload = 'groupids[]={}'.format(self.id)
        userids = Moodle().submit_request('core_group_get_group_members', payload)
        self.userids = userids[0]['userids']
        return self.userids