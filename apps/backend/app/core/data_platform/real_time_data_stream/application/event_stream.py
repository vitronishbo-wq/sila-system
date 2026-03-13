class RealTimeDataStream:

    def __init__(self):

        self.subscribers = {}

    def publish(

        self,
        topic,
        event

    ):

        consumers = self.subscribers.get(topic, [])

        for consumer in consumers:
            consumer(event)

    def subscribe(

        self,
        topic,
        handler

    ):

        if topic not in self.subscribers:
            self.subscribers[topic] = []

        self.subscribers[topic].append(handler)
