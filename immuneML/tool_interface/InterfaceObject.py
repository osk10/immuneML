import json


class InterfaceObject:

    def __init__(self, main_function_name):
        self.main_function_name = main_function_name  # testing call of function name

    def _toJson(self):
        # make object JSON serializable
        jsonData = json.dumps(self, default=lambda o: o.__dict__)
        print(f"Producing json data in interface: {jsonData}")
        return jsonData

    def getJson(self):
        return self._toJson()