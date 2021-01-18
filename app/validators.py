class EventsValidator:
    def validateGetEvent(name):
        if type(name) == str:
            return True
        return False

    def validateAddEvent(data):
        if "name" in data and "description" in data and "state" in data:
            return True
        return False