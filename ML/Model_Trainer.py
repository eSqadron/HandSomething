

PARAM_NAMES = ['Rock', 'Led', 'Door', 'Cart']


if __name__ == '__main__':
    x_train = []
    y_train = []

    for param in PARAM_NAMES:
        try:
            with open(f"{param}.txt", 'r') as f:
                lines = f.readlines()
                for line in lines:
                    r_line = line.replace('[', '').replace(']', '').replace(' ', '')
                    line_ints = [int(i) for i in  r_line.split(',')]
                    x_train.append(line_ints)
                    y_train.append(param)
        except FileNotFoundError:
            pass

    # TUTAJ UCZENIE
    print(x_train)
    print(y_train)
