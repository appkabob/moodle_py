try:
    import constants
except ImportError:
    pass
from .moodle_utils import Moodle


class Email:
    def __init__(self, to_user, body):
        self.to_user = to_user
        self.body = body

    def send(self, is_test=False):
        if is_test:  # for testing purposes, send to admin user instead of would-be recipient
            payload = 'messages[0][touserid]={}&messages[0][text]={}'.format(constants.ADMIN_USER_ID, self.body)
        else:
            payload = 'messages[0][touserid]={}&messages[0][text]={}'.format(self.to_user.userid, self.body)
        return Moodle().submit_request('core_message_send_instant_messages', payload)
