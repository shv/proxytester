from .base import BaseProcess


class Process(BaseProcess):
    def __call__(self, result):
        project = self.current_case.project
        self.variables = project.get_variables()
        self.apply_format(result)
        return result

    def apply_format(self, subtree):
        for key in subtree:
            if isinstance(subtree[key], dict):
                self.apply_format(subtree[key])
            elif isinstance(subtree[key], list):
                for i in range(len(subtree[key])):
                    self.apply_format(subtree[key][i])
            elif isinstance(subtree[key], str):
                subtree[key] = subtree[key] % self.variables
