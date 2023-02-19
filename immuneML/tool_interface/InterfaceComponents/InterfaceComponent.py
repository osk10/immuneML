from abc import ABC, abstractmethod
import json


class InterfaceComponent(ABC):
    # The other components should inherit from this
    # Should contain functions that can be reused or overwritten

    @staticmethod
    def produce_JSON_object(**input_data):
        # **input_data = dictionary of keyword arguments
        print("Printing input sent to function produce_JSON_object")
        for key, value in input_data.items():
            print(f"Key: {key}, value: {value}")

        try:
            json_bytes = json.dumps(input_data)
        except Exception as e:
            print(f"Error: {e}")
            return

        return json_bytes
