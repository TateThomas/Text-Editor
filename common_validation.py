
class CommonValidation:

    @staticmethod
    def validate_type(inst, clss):
        if isinstance(inst, clss):
            return inst
        raise TypeError(f"{inst} is not an instance of {clss}")
