import requests


def upload_file_to_channel(
    bot_token: str,
    chat_id: str,
    file_path: str,
    caption: str = "",
):
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    data = {"chat_id": chat_id, "caption": caption}

    with open(file_path, "rb") as file:
        files = {"document": file}
        response = requests.post(url, data=data, files=files)

    print(response.json())
    return response.json()
