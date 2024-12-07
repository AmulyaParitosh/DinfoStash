import requests

from ..data.constants import ImagePath


def download_img(image_url: str, image_name: str):
    img_data = requests.get(image_url).content
    with open(image_name, "wb") as handler:
        handler.write(img_data)


def check_image_url(url: str | ImagePath) -> bool:
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
