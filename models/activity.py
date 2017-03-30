class Activity:
    def __init__(self, userid, status):
        self.userid = userid
        self.status = status

    def __repr__(self):
        return "<Activity cmid {} state {}>".format(self.status['cmid'], self.status['state'])
