class StepManager:
    def __init__(self):
        pass

    def getSteps(self, level: int):
        if level == 1:
            return [
                ["Mitte", "Links"],
                ["Mitte"],
                ["Mitte", "Rechts"],
                ["Mitte"],
                ["Mitte", "Links"],
                ["Mitte"],
                ["Mitte", "Rechts"],
                ["Mitte"]
            ]
        elif level == 2:
            return [
                ["Mitte", "Vorne"],
                ["Mitte"],
                ["Mitte", "Hinten"],
                ["Mitte"],
                ["Mitte", "Vorne"],
                ["Mitte"],
                ["Mitte", "Hinten"],
                ["Mitte"]
            ]
        elif level == 3:
            return [
                ["Mitte", "Links"],
                ["Mitte"],
                ["Mitte", "Rechts"],
                ["Mitte"],
                ["Mitte", "Vorne"],
                ["Mitte"],
                ["Mitte", "Hinten"],
                ["Mitte"]
            ]
        elif level == 4:
            return [
                ["Mitte", "Links"], ["Mitte"], ["Mitte", "Rechts"], ["Mitte"],
                ["Mitte", "Links"], ["Mitte"], ["Mitte", "Rechts"], ["Mitte"],
                ["Mitte", "Vorne"], ["Mitte"], ["Mitte", "Hinten"], ["Mitte"],
                ["Mitte", "Vorne"], ["Mitte"], ["Mitte", "Hinten"], ["Mitte"],
                ["Mitte", "Links"], ["Mitte"], ["Mitte", "Rechts"], ["Mitte"],
                ["Mitte", "Links"], ["Mitte"], ["Mitte", "Rechts"], ["Mitte"],
                ["Mitte", "Vorne"], ["Mitte"], ["Mitte", "Hinten"], ["Mitte"],
                ["Mitte", "Vorne"], ["Mitte"], ["Mitte", "Hinten"], ["Mitte"]
            ]
        elif level == 5:
            return [
                ["Mitte", "Links"], ["Mitte"], ["Mitte", "Rechts"], ["Mitte"],
                ["Mitte", "Vorne"], ["Mitte"], ["Mitte", "Hinten"], ["Mitte"],
                ["Mitte", "Vorne"], ["Mitte"], ["Mitte", "Hinten"], ["Mitte"],
                ["Mitte", "Links"], ["Mitte"], ["Mitte", "Rechts"], ["Mitte"],
                ["Mitte", "Vorne"], ["Mitte"], ["Mitte", "Hinten"], ["Mitte"],
                ["Mitte", "Links"], ["Mitte"], ["Mitte", "Rechts"], ["Mitte"],
                ["Mitte", "Links"], ["Mitte"], ["Mitte", "Rechts"], ["Mitte"],
                ["Mitte", "Vorne"], ["Mitte"], ["Mitte", "Hinten"], ["Mitte"]
            ]
        else:
            return ["Unbekanntes Level – keine Schritte definiert"]

