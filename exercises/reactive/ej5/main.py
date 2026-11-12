import os
import subprocess as shell
from typing import Any

import requests
from dotenv import load_dotenv
from reactivex import of
from reactivex import operators as ops

load_dotenv()
API_KEY = os.getenv("key")


def get_api_data(title: str, key: str | None) -> dict[str, Any]:
    if not key:
        raise KeyError("API key not found in .env")
    return requests.get(f"https://www.omdbapi.com/?t={title}&apikey={key}").json()


def validate_response(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("Response") != "True":
        raise ValueError(data.get("Error", "Error desconocido en la API"))
    return data


def show_info(data: dict[str, Any]) -> str:
    return (
        f"Title: {data['Title']}\n"
        f"Director: {data['Director']}\n"
        f"Released: {data['Released']}\n"
        f"Rating: {data['imdbRating']}\n"
        f"Plot: {data['Plot']}"
    )


def show_poster(data: dict[str, Any]) -> None:
    shell.run(["kitten", "icat", data["Poster"]])


def download_poster(data: dict[str, Any]) -> None:
    url: str = data["Poster"]
    name: str = ".".join([data["Title"], url.split(".")[-1]])
    shell.run(["curl", "-L", "-s", url, "-o", name])


def show_error(error: Exception) -> None:
    print("ERROR:", error)


if __name__ == "__main__":
    movie_title = input("Movie name: ")

    t_observable = of(movie_title).pipe(
        ops.map(lambda title: get_api_data(title, API_KEY)),
        ops.map(validate_response),
        ops.do_action(show_poster),
        ops.map(show_info))

    t_observable.subscribe(
        on_next=print,
        on_error=show_error,
    )
