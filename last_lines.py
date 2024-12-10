def last_lines(file: str):
    with open(file, "r") as f:
        for line in f.read().splitlines(True)[::-1]:
            if line:
                yield line
