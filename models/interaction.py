

class Interaction:
    def __init__(self, _id, slide_id, latency, result, student_response, time, type, weighting):
        self.id = _id
        self.slide_id = slide_id
        self.latency = latency
        self.result = result
        self.student_response = student_response
        self.time = time
        self.type = type
        self.weighting = weighting

    def __repr__(self):
        return '<Interaction {}>'.format(self.slide_id)