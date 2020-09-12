import datetime

from source.util.ReflectionHandler import ReflectionHandler
from source.workflows.instructions.Instruction import Instruction


class SemanticModel:

    def __init__(self, instructions: list, path, output=None):
        assert all(isinstance(instruction, Instruction) for instruction in instructions), \
            "SemanticModel: error occurred in parsing: check instruction definitions in the configuration file."
        self.instructions = instructions
        self.path = path
        self.output = output

    def run(self):
        instruction_states = self.run_instructions()
        if self.output is not None:
            self.build_reports(instruction_states)
        return instruction_states

    def build_reports(self, instruction_states):
        report_builder = self.make_report_builder()
        print(f"{datetime.datetime.now()}: Generating {self.output['format']} reports...")
        path = report_builder.build(instruction_states, self.path)
        print(f"{datetime.datetime.now()}: {self.output['format']} reports are generated.")
        return path

    def run_instructions(self) -> list:
        instruction_states = []
        for index, instruction in enumerate(self.instructions):
            print("{}: Instruction {}/{} has started.".format(datetime.datetime.now(), index+1, len(self.instructions)))
            result = instruction.run(result_path=self.path)
            instruction_states.append(result)
            print("{}: Instruction {}/{} has finished.".format(datetime.datetime.now(), index+1, len(self.instructions)))
        return instruction_states

    def make_report_builder(self):
        report_builder = ReflectionHandler.get_class_by_name(f"{self.output['format']}Builder", "presentation/")
        return report_builder
