from functools import reduce


def factorial(num: int) -> int:
    return reduce(lambda x, y: x*y, range(1, num+1))


if __name__ == "__main__":
    print(factorial(5))
