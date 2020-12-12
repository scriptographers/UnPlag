def fibonacci_memo(input_value):
    fibonacci_cache = {}
    if input_value in fibonacci_cache:
        return fibonacci_cache[input_value]
    if input_value == 1:
            value = 1
    elif input_value == 2:
            value = 1
    elif input_value > 2:           
            value =  fibonacci_memo(input_value -1) + fibonacci_memo(input_value -2)
    fibonacci_cache[input_value] = value
    return value

for i in range(1, 201):
     print("fib({}) = ".format(i), fibonacci_memo(i))