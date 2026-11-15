def square_sum(num: int) -> int:
    return sum(map(lambda x: x**2, range(1, num)))


if __name__ == "__main__":
    print(square_sum(9))
