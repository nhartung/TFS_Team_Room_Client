class Room():
    def __init__(self, name, description, lastActivity):
        self.name = name
        self.description = description
        self.lastActivity = lastActivity


    def __str__(self):
        return f'[name: {self.name}, description: {self.description}, lastActivity: {self.lastActivity}]'

