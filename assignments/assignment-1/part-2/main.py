from enum import StrEnum
from hashlib import sha1
import requests
from typing import Any, Callable, NamedTuple


class ApiPetitions(StrEnum):
    PasswdNTLM = "https://api.pwnedpasswords.com/range/{}?mode=ntlm"
    PasswdSHA1 = "https://api.pwnedpasswords.com/range/{}"
    Domain = "https://haveibeenpwned.com/api/v3/breaches?Domain={}"


PARSER: dict[ApiPetitions, Callable] = {ApiPetitions.PasswdNTLM: .text, PasswdSHA1: .text, Domain: .json()}


class ApiResponse(NamedTuple):
    ok: bool
    data: Any = None
    error: str | None = None


def texto_to_dict(text: str) -> dict[str, Any]:
    return dict(map(lambda item: (item[0], int(item[1])), map(lambda line: line.split(":"), text.splitlines())))


def get_api_data(petition: str, arg: str) -> ApiResponse:
    response = requests.get(petition.format(arg))

    if response.ok:
        return ApiResponse(ok=True, data=response)
    else:
        return ApiResponse(ok=False, error=f"Error: {response.status_code}")


def manage_data(data: dict[str, Any], on_succes: Callable, on_error: Callable) -> str:
    if data:
        return on_succes(data)
    else:
        return on_error(data)


def get_passwd(data: dict[str, Any], passwd: str) -> str:
    breach = data.get(passwd)
    if breach:
        return f"Password breached {breach} times"
    else:
        return "Password not breached"


if __name__ == "__main__":
    hash_sha1 = sha1(input("password: ").encode("utf-8")).hexdigest()
    manage_data(get_api_data(ApiPetitions.PasswdSHA1,
                             hash_sha1[:5]), get_passwd, print)
    # print(get_api_data(ApiPetitions.PasswdSHA1, hash_sha1[:5]))
    # print(get_api_data(ApiPetitions.Domain, input()))
