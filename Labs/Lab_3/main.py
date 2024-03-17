import test

print("Press 'q' if you want to quit.")
while True:
    text = input('test > ')
    result, errors = test.run('<stdin>', text)

    if errors:
        for err in errors:
            print(err.as_string())
    else:
        for token in result:
            print(token)

    user_input = input()
    if user_input.lower() == 'q':
        break
