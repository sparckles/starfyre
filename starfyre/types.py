class Component:
    def __init__(self, pyml: str) -> Node:
        self.pyml = pyml

        return create_component(self.pyml)

