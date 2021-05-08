import argparse

import requests

parser = argparse.ArgumentParser(
    prog="uptobox_backup",
    description="Backup the content of an uptobox account to another",
)
parser.add_argument(
    "token1",
    metavar="token1",
    type=str,
    help="Token for the first account",
)
parser.add_argument(
    "token2",
    metavar="token2",
    type=str,
    help="Token for the second account",
)
parser.add_argument(
    "path",
    metavar="path",
    type=str,
    help="Path to copy",
)
args = parser.parse_args()

token1 = args.token1  # uptobox token of the old account
token2 = args.token2
path = args.path  # uptobox token of the new account


def alias_path(path):
    print(f"{path=}")
    params_init = {
        "token": token1,
        "orderBy": "file_name",
        "dir": "asc",
        "offset": 0,
        "path": path,
        "limit": 100,
    }
    init_res = requests.get(
        "https://uptobox.com/api/user/files",
        params=params_init,
    )
    loaded_json = init_res.json()
    try:
        page_counter = loaded_json["data"]["pageCount"]
        folders = [folder["fld_name"] for folder in loaded_json["data"]["folders"]]
    except TypeError:
        print(init_res.url)
        raise RuntimeError(
            f"Code {loaded_json['statusCode']}: {loaded_json['message']} 1"
        )

    for page in range(page_counter):
        param_file_list = {
            "token": token1,
            "orderBy": "file_name",
            "dir": "asc",
            "offset": str(page * 100),
            "path": path,
            "limit": 100,
        }
        file_list_res = requests.get(
            "https://uptobox.com/api/user/files", params=param_file_list
        )
        loaded_file_list = file_list_res.json()
        for file in loaded_file_list["data"]["files"]:
            print(f"{file['file_name']} (https://uptobox.com/{file['file_code']}/)")
            params_alias = {"token": token2, "file_code": file["file_code"]}
            res = requests.get(
                "https://uptobox.com/api/user/file/alias", params=params_alias
            )
            data = res.json()
            if data["statusCode"] != 0:
                raise RuntimeError(f"Code {data['statusCode']}: {data['message']} 2")
    for folder in folders:
        alias_path(folder)


def main():
    pass


if __name__ == "__main__":
    alias_path(path)
