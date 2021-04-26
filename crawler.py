import os.path
import re
import requests
import time
from fake_useragent import UserAgent

headers = {'User-Agent': UserAgent().firefox}
data_directory = 'data'
twic_url = 'https://theweekinchess.com/twic'


def read_main_page():
    resp = requests.get(twic_url, headers=headers)
    if resp.status_code == 200:
        return resp.text


def read_response_from_file():
    with open("twic.html", 'r') as f:
        return f.read()


def data_path(filename: str):
    return data_directory + '/' + filename


def file_exists(filename: str):
    return os.path.isfile(data_path(filename))


def main():
    f = read_main_page()
    sites = [(site.split('/')[-1], site)
             for site in re.findall(r'https.*g.zip', f)]
    sites_to_download = []
    print(f'Total weeks found: {len(sites)}, '
          f'missing weeks to download: {len(sites_to_download)}')

    for filename, site in sites:
        if not file_exists(filename):
            sites_to_download.append((filename, site))

    for idx, (filename, site) in enumerate(sites_to_download):
        print('wait 3 seconds before download')
        time.sleep(3)
        print(f'download [{idx+1}/{len(sites_to_download)}] {site} '
              'save to {filename}')
        resp = requests.get(site, headers=headers)
        if resp.status_code == 200:
            if not os.path.isfile(filename):
                with open(data_path(filename), 'wb') as f:
                    f.write(resp.content)
            else:
                print(f'file conflict: {site}, {filename}')
        else:
            print(f'status: {resp.status_code}')


if __name__ == '__main__':
    main()
