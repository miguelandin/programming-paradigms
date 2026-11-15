def palindromes(words: list[str]) -> list[bool]:
    return list(map(is_palindrome, words))


def is_palindrome(word: str) -> bool:
    palindrome = True
    o: int = 0
    e: int = len(word) - 1

    while o != e:
        if word[o] != word[e]:
            palindrome = False
            break
        o += 1
        e -= 1

    return palindrome


if __name__ == "__main__":
    words: list = ["ana", "reconocer", "oso",
                   "hola", "mundo", "luzazul"]

    print(palindromes(words))
