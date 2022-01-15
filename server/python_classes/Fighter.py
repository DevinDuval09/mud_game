from Character import Character
class Fighter(Character):
    def __init__(self, style, *args, **kwargs):
        super.__init__(*args, **kwargs)
        if (style == "archery"):
            pass
        elif (style == "dueling"):
            pass
        elif (style == "defense"):
            pass
        elif (style == "gw_fighting"):
            pass
    
    def heal(self):
        pass

    def surge(self):
        pass

    def resist(self):
        pass