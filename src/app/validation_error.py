class ValidationError:
    def __init__(self, field_name, violated_constraint):
        self.error_message = f"{field_name} is not valid due to {violated_constraint}"
