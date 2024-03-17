import test

# Run loop
print("Press 'q' if you want to quit.")
while True:
    text = input('test > ')
    result, error = test.run('<stdin>', text)

    if error:
        for err in error:
            print(err.as_string())
    else:
        print(result)

    user_input = input()
    if user_input.lower() == 'q':
        break