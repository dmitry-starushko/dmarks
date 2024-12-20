

def create_market(mid: str, data):
    match data:
        case {
            # must match Market model
        }:
            # create Market here
            return True
        case _:
            raise ValueError(data)
