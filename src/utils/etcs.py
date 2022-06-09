import random
import string


def random_id() -> str:
    """
    Generate random id.
    :return: random id
    """
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(10)]
    )
