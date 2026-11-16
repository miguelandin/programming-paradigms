from enum import StrEnum
import requests
from typing import Any, Callable, NamedTuple
import json
from functools import partial
import argparse
from getpass import getpass
from Crypto.Hash import SHA1, MD4


def text_to_dict(text: str) -> dict[str, Any]:
    return dict(map(lambda item: (item[0], int(item[1])), map(lambda line: line.split(":"), text.splitlines())))


class Ption(StrEnum):
    PasswdNTLM = "https://api.pwnedpasswords.com/range/{}?mode=ntlm"
    PasswdSHA1 = "https://api.pwnedpasswords.com/range/{}"
    Domain = "https://haveibeenpwned.com/api/v3/breaches?Domain={}"


class Color(StrEnum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    PURPLE = "\033[95m"
    RESET = "\033[0m"


def paint(text: str, color: Color) -> str:
    return f"{color}{text}{Color.RESET}"


PARSERS: dict[Ption, Callable[[str], Any]] = {
    Ption.PasswdNTLM: text_to_dict,
    Ption.PasswdSHA1: text_to_dict,
    Ption.Domain: json.loads,
}


class ApiResponse(NamedTuple):
    ok: bool
    data: Any = None
    error: str | None = None


def get_api_data(petition: Ption, arg: str) -> ApiResponse:
    response = requests.get(petition.format(arg))

    if response.ok:
        return ApiResponse(ok=True, data=PARSERS[petition](response.text))
    else:
        return ApiResponse(ok=False, error=f"Error: {response.status_code}")


def manage_data(data: ApiResponse, on_succes: Callable, on_error: Callable) -> str:
    if data.ok:
        return on_succes(data.data)
    else:
        return on_error(data.error)


def get_error(error: str) -> str:
    return paint(f"[!] {error}", Color.RED)


def get_passwd_info(data: dict[str, Any], passwd: str) -> str:
    breach = data.get(passwd[5:])
    if breach:
        return paint(f"Password breached {breach} times", Color.RED)
    else:
        return paint("Password not breached", Color.GREEN)


def parse_domain_breach(data: dict[str, Any]) -> str:
    title = paint(data.get("Title", ""), Color.CYAN)
    breach_date = paint(data.get("BreachDate", ""), Color.PURPLE)
    description = paint(data.get("Description", ""), Color.RED)

    return f"Title: {title}\n Breach date: {breach_date}\n Description: {description}"


def get_domain_info(data: list[dict[str, Any]]) -> str:
    if (data):
        return "\n\n".join(map(parse_domain_breach, data))
    else:
        return paint("No breaches found", Color.GREEN)


def sha1(raw_passwd: str) -> str:
    return SHA1.new(raw_passwd.encode(
        "utf-8")).hexdigest().upper()


def ntlm(raw_passwd: str) -> str:
    return MD4.new(raw_passwd.encode(
        "utf-16le")).hexdigest().upper()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Breach Checker")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--password", action="store_true",
                       help="Check if password has been leaked")

    group.add_argument(
        "-d", "--domain", help="Check if domain had a data breach")

    parser.add_argument("--ntlm", action="store_true",
                        help="Use NTLM  instead of SHA1")

    args = parser.parse_args()

    if args.password:
        hasher, endpoint = (ntlm, Ption.PasswdNTLM) if args.ntlm else (
            sha1, Ption.PasswdSHA1)
        passwd = hasher(getpass("Password: "))
        print(manage_data(get_api_data(endpoint, passwd[:5]), partial(
            get_passwd_info, passwd=passwd), get_error))
    elif args.domain:
        print(manage_data(get_api_data(Ption.Domain,
              args.domain), get_domain_info, get_error))
