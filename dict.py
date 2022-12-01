def find(d, path):
    if not path:
        return list(d.keys())
    for k, v in d.items():
        if k == path[0]:
            if isinstance(v, dict):
                return find(v, path[1:])
            elif len(path) == 1:
                return v
            else:
                return []


def push(d, path, key, value):
    if not path:
        if isinstance(d, dict):
            d[key] = value
        else:
            d.append(value)
        return
    for k, v in d.items():
        if k == path[0]:
            if isinstance(v, dict) or isinstance(v, list):
                push(v, path[1:], key, value)
