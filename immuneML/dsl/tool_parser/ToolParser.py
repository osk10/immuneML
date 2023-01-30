class ToolParser:

    @staticmethod
    def parse(workflow_specification: dict):

        specs = workflow_specification["tools"]

        print(f"workflow_specification: {specs}")