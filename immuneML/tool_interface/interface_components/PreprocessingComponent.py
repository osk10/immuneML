from immuneML.tool_interface.interface_components.InterfaceComponent import InterfaceComponent


class PreprocessingComponent(InterfaceComponent):

    def __init__(self, name: str, specs: dict):
        super().__init__(name, specs)

    def run_component(self):
        # Preprocessing is applied to modify a dataset before encoding the data
        pass
