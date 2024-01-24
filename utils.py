import pathlib
import yaml
import csv
from urllib.request import urlopen


def read_file(path: str | pathlib.Path) -> str:
    path = pathlib.Path(path)

    try:
        with open(path.resolve().as_posix()) as f:
            data = f.read()
    except (Exception,):
        print('Error with read ... ')
        return

    return data


def write_file(path: str | pathlib.Path, data, mode='w+') -> pathlib.Path | None:
    path = pathlib.Path(path)
    try:
        with open(path.resolve().as_posix(), mode) as f:
            f.write(data)
    except (Exception,):
        print('Error with write .... ')
        return

    return path


def read_yaml(path: str | pathlib.Path):
    text = read_file(path)
    return yaml.load(text, Loader=yaml.Loader)


def write_yaml(path: str | pathlib.Path, data) -> pathlib.Path | None:
    text = yaml.dump(
        data,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
    )
    return write_file(path, text)


def download_csv(url):
    csv_reader = []
    try:
        response = urlopen(url)
        lines = [line.decode('utf-8') for line in response.readlines()]
        csv_reader = csv.reader(lines, delimiter=',')
    except (Exception,):
        print('Error download_csv')
        return []
    
    return [row for row in csv_reader]

