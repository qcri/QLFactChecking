
class Comment:

    def __init__(self, qid, cid, qcategory, qsubject, qbody, ctext, cuser, cdate):
        self.question_id = qid
        self.comment_id = cid
        self.qcategory = qcategory
        self.qsubject = qsubject
        self.qbody = qbody
        self.text = ctext
        self.user = cuser
        self.date = cdate
        self.label = 0
        self.predicted_label = 0