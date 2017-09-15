

class Interaction:
    def __init__(self, _id, userid, slide_id, result, student_response, time, type, weighting):
        self.id = _id
        self.userid = userid
        self.slide_id = slide_id
        self.result = result
        self.student_response = student_response
        self.time = time
        self.type = type
        self.weighting = weighting

    def __repr__(self):
        return '<Interaction {}>'.format(self.slide_id)
