while True:
    try:
        line = input()
        if line.strip():
            print(line)
    except EOFError:
        break

    