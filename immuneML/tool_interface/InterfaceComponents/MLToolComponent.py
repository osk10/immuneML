from immuneML.tool_interface.InterfaceComponents.InterfaceComponent import InterfaceComponent


class MLToolComponent(InterfaceComponent):

    @staticmethod
    def instruction_handler(specs: dict):
        print(f"MLToolComponent received specs: {specs}")
