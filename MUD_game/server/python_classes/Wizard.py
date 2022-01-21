from Character import Character
class Wizard(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def recover(self):
        pass
    
    def cast(self):
        pass
