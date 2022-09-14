from tests.constants import TEST_DATA_DIR
from urllib.parse import urlparse
import requests
from os import path


def get_file(file_url):
    """A function to get a file from a path or from a URL in case it is absent.
    Files are saved in a local directory for future reuse"""

    temp_dir = path.abspath(TEST_DATA_DIR)
    parsed_url = urlparse(file_url)
    file_name = parsed_url.path.split('/')[-1]
    full_path = path.join(temp_dir, file_name)
    if not path.exists(full_path):
        r = requests.get(file_url)
        open(full_path, 'wb').write(r.content)

    return full_path
