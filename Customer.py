from Judge import Judge


class Customer(object):

    @staticmethod
    def customer(q):
        while True:
            submission = q.get()
            Judge(submission)
