def preprocessing_filter_spec(endpoints):
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        if path.startswith("/extapi/"):
            filtered.append((path, path_regex, method, callback))
    return filtered


