import os
from typing import Callable
import requests
from dotenv import load_dotenv
from typing import Any
import subprocess as shell

load_dotenv()

API_KEY = os.getenv("key")


def show_info(data: dict):
    print("Movie: ", data["Title"])
    print("Director: ", data["Director"])
    print("Released: ", data["Released"])
    print("Rating: ", data["imdbRating"])
    print("Plot: ", data["Plot"])


def show_poster(data: dict[str, Any]):
    shell.run(["kitten", "icat", data["Poster"]])


def download_poster(data: dict[str, Any]):
    url: str = data["Poster"]
    name: str = data["Title"] + '.' + url.split('.')[-1]
    shell.run(["curl", "-L", url, "-o", name])


def show_error(message: str):
    print("ERROR: ", message)


def get_api_data(title: str, key: str | None) -> dict:
    if not key:
        raise KeyError("API key not found in .env")

    return requests.get(f"https://www.omdbapi.com/?t={title}&apikey={key}").json()


def get_movie_data(api_data: dict, on_succes: Callable, on_error: Callable):
    if api_data["Response"] == "True":
        on_succes(api_data)
    else:
        on_error(api_data["Error"])


if __name__ == "__main__":
    data = get_api_data(input("Movie name: "), API_KEY)
    get_movie_data(data, show_info, show_error)
    get_movie_data(data, show_poster, show_error)
    get_movie_data(data, download_poster, show_error)
