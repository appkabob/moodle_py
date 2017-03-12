import requests
import constants


class Moodle:
    def __init__(self):
        self.interactions = []

    @staticmethod
    def submit_request(wsfunction, payload, verb='POST'):
        # url = '{}?wstoken={}&moodlewsrestfromat={}&wsfunction={}'.format(constants.MOODLE_QUERY_URL,
        #                                                                constants.WSTOKEN,
        #                                                                constants.MOODLEWSRESTFORMAT, wsfunction)
        querystring = {"wstoken": constants.WSTOKEN, "moodlewsrestformat": "json",
                       "wsfunction": wsfunction}
        r = requests.post(url=constants.MOODLE_QUERY_URL, data=payload, headers=constants.HEADERS, params=querystring)

        if r.status_code == requests.codes.ok or r.status_code == 201:
            print(r)
            return r.json()

        print('error', r)
        return r.message