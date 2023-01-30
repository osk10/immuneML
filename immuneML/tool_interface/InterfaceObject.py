import json

class InterfaceObject:

    def __init__(self, main_function_name):
        self.main_function_name = main_function_name

    def toJson(self):
        # make object JSON serializable
        return json.dumps(self, default=lambda o: o.__dict__)