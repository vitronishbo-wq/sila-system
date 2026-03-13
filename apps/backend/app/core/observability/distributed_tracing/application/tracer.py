import uuid
import time


class SovereignTracer:

    def __init__(self):

        self.traces = {}

    def start_trace(self, service_name):

        trace_id = str(uuid.uuid4())

        self.traces[trace_id] = {

            "service": service_name,
            "start_time": time.time(),
            "spans": []

        }

        return trace_id

    def add_span(

        self,
        trace_id,
        operation

    ):

        span = {

            "operation": operation,
            "timestamp": time.time()

        }

        self.traces[trace_id]["spans"].append(span)

    def end_trace(self, trace_id):

        self.traces[trace_id]["end_time"] = time.time()

        return self.traces[trace_id]
