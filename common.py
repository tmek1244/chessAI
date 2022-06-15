def translate(key) -> tuple[int, int]:
    mapping = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }

    if isinstance(key, tuple):
        return key[0], key[1]
    if isinstance(key, str):
        return int(key[1]) - 1, mapping[key[0]]
