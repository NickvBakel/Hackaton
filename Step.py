class Step(object):
    kind = ""
    departure_location = ""
    arrival_location = ""
    departure_time = ""
    arrival_time = ""
    duration = ""

    def __init__(self, kind="", departure_location="", arrival_location="", departure_time="", arrival_time="",
                 duration=""):
        self.kind = kind
        self.departure_location = departure_location
        self.arrival_location = arrival_location
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration

    def show(self):
        print(',\n'.join("%s: %s" % item for item in vars(self).items()))
