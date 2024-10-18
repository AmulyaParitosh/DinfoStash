import requests


def download_img(image_url: str, image_name: str):
    img_data = requests.get(image_url).content
    with open(image_name, "wb") as handler:
        handler.write(img_data)
