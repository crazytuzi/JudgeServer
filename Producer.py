class Producer(object):
    @staticmethod
    def producer(q, data):
        q.put(data)
