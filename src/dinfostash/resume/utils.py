import requests

from dinfostash.data.constants import ImagePath


def download_img(image_url: str, image_name: str):
    try:
        img_data = requests.get(image_url).content
    except requests.exceptions.InvalidSchema as exp:
        raise ValueError("Invalid url") from exp
    with open(image_name, "wb") as handler:
        handler.write(img_data)


def check_image_url(url: str | ImagePath) -> bool:
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
