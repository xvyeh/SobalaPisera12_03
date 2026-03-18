from pydantic import ValidationError


def parse_errors(e: ValidationError):
    errors = []
    for err in e.errors():
        errors.append({
            "loc": err["loc"],
            "msg": err["msg"]
        })
    return errors
