from transitions.extensions import GraphMachine
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

machine = TocMachine(
    states=["user", "input_2currency", "check", "calculate", "input_number"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "input_2currency",
            "conditions": "is_going_to_input_2currency",
        },
        {
            "trigger": "advance",
            "source": "input_2currency",
            "dest": "check",
            "conditions": "is_going_to_check",
        },
        {
            "trigger": "advance",
            "source": "input_2currency",
            "dest": "calculate",
            "conditions": "is_going_to_calculate",
        },
        {
            "trigger": "advance",
            "source": "calculate",
            "dest": "input_number",
            "conditions": "is_going_to_input_number",
        },
        {"trigger": "go_back", "source": ["check", "input_number", "calculate", "input_2currency"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)


machine.get_graph().draw("fsm.png", prog="dot", format="png")
