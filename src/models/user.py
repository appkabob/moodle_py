from .moodle_utils import Moodle


class User:
    def __init__(self, userid, username, email, firstname, lastname, iein=None):
        self.userid = userid
        # self.userfullname = userfullname
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.iein = iein

    def __repr__(self):
        return '<User {} {}>'.format(self.userid, self.username)

    @classmethod
    def get_users_for_course(cls, courseid):
        payload = 'courseid={}'.format(courseid)
        users_list = Moodle().submit_request('gradereport_user_get_grades_table', payload)
        users_objs = []
        for user in users_list['tables']:
            # if "On-Demand Module Part 3" in str(user['tabledata']):
            users_objs.append(cls(user['userid'], user['userfullname']))
        return users_objs

    @classmethod
    def get_users_enrolled(cls, courseid):
        payload = 'courseid={}&options[0][name]=onlyactive&options[0][value]=1'.format(courseid)
        users_list = Moodle().submit_request('core_enrol_get_enrolled_users', payload)
        users_objs = []
        for user in users_list:
            iein = None
            if 'customfields' in user.keys():
                for field in user['customfields']:
                    if field['shortname'] == 'iein':
                        iein = field['value']
                users_objs.append(cls(
                    user['id'],
                    user['username'],
                    user['email'],
                    user['firstname'],
                    user['lastname'],
                    iein
                ))
        return users_objs
