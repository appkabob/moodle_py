from models.moodle_utils import Moodle


class Email:
    def __init__(self, to_user, body):
        self.to = to_user
        self.body = body


class BCYouShouldLiveChatEmail(Email):
    def __init__(self, to_user, dateandtimeofnextlivechat, numberofenrollmentdays='60'):
        Email.__init__(self, to_user, body=None)
        self.to_user = to_user
        self.dateandtimeofnextlivechat = dateandtimeofnextlivechat
        self.numberofenrollmentdays = numberofenrollmentdays
        self.body = self._read_body_from_template()

    def _read_body_from_template(self):
        with open('email_templates/BCYouShouldLiveChatEmail.txt', 'r') as f:
            read_data = f.read()
        return read_data.replace('\n', '<br />').\
            replace('{numberofenrollmentdays}', self.numberofenrollmentdays).\
            replace('{dateandtimeofnextlivechat}', self.dateandtimeofnextlivechat)

    def send(self):
        payload = 'messages[0][touserid]={}&messages[0][text]={}'.format(self.to_user.userid, self.body)
        email = Moodle().submit_request('core_message_send_instant_messages', payload)
        return email