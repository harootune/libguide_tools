# stdlib
import csv
import urllib.parse as parse
from typing import List
from pathlib import Path


def assemble_absolute_link(origin: str, path: str) -> str:
    """
    Checks if a link is absolute
    :param origin: the address of the page where an image src was linked from
    :param path: an image src
    :return: an absolute version of the link, if it is not already absolute
    """
    src_parts = parse.urlparse(path)
    if not src_parts.netloc:
        return parse.urljoin(origin, path)
    else:
        return path


def links_from_libguide_csv(path: str) -> List[str]:
    url_list = []

    filepath = Path(path)
    with open(filepath, newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        headers = reader.__next__()
        url_index = headers.index('URL')
        if not url_index:
            url_index = -1

        for row in reader:
            url_list.append(row[url_index])

    return url_list
