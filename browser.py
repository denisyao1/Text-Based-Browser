# imports
import os as OS
import sys
from collections import deque

import bs4
import requests
from colorama import Fore, init, deinit

dirName = sys.argv[1]


def create_dir(directory) -> None:
    if not OS.path.exists(directory):
        OS.mkdir(directory)
        # print(f"directory {directory} created")
    # else:
    # print(f"directory {directory} Already Exits")


# def encode_utf_8(st: str) -> str:
#     _bytes = st.encode('UTF-8', errors='ignore')
#     _s = _bytes.decode('UTF-8', errors='ignore')
#
#     return _s


def save_webpage(_url: str, soup: bs4.BeautifulSoup) -> None:
    filename = dirName + '\\' + transform_url(_url) + '.txt'
    if not OS.path.isfile(filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(save_soup(soup))
            f.close()


def transform_url(_url: str) -> str:
    url_split = _url.split('.')
    st = ".".join(url_split[:-1])

    return st


def check_File(_url: str) -> bool:
    filename = dirName + '\\' + _url + ".txt"
    # print(">> filename : " + filename)
    if OS.path.isfile(filename):
        # print(f" {filename} exits")
        return True
    else:
        # print(f"{filename} not exits")
        return False


def print_soup(sp: bs4.BeautifulSoup) -> str:
    tags_list = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li']
    for child in sp.body.descendants:
        if child is not bs4.element.NavigableString:
            # print(f" >> {child.name}")
            if child.name in tags_list:
                if child.name == 'a':
                    for string in child.stripped_strings:
                        print(Fore.BLUE + string)
                else:
                    for string in child.stripped_strings:
                        print(Fore.LIGHTWHITE_EX + string)


def save_soup(sp: bs4.BeautifulSoup) -> str:
    tags_list = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li']
    result = ''
    for child in sp.body.descendants:
        if child is not bs4.element.NavigableString:
            # print(f" >> {child.name}")
            if child.name in tags_list:
                for string in child.stripped_strings:
                    result += string + "\n"
    return result


def print_file(_url: str) -> None:
    # filename = dirName + '\\' + sitename + ".txt"
    # tags_list = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li']
    #
    # for child in sp.body.descendants:
    #     if child is not bs4.element.NavigableString:
    #         # print(f" >> {child.name}")
    #         if child.name in tags_list:
    #             if child.name == 'a':
    #                 print(Fore.BLUE + f" >> {child.name}")
    #                 for string in child.stripped_strings:
    #                     print(Fore.BLUE + string)
    #             else:
    #                 for string in child.stripped_strings:
    #                     print(Fore.LIGHTWHITE_EX + string)
    filename = dirName + '\\' + transform_url(_url) + '.txt'
    with open(filename, 'r', encoding='UTF-8') as f:
        print(f.read())


def send_request(_url: str):
    # if not _url.startswith("www."):
    #     _url = "www." + _url
    copy_url = _url
    if not copy_url.startswith("https://"):
        copy_url = "https://" + copy_url
    # print(">> copy of url : " + copy_url + " >> url : " + _url)
    resp = requests.get(copy_url)
    return resp

def gotoWebsite(_url) -> None:
    if _url.__contains__('.'):
        if not check_File(transform_url(_url)):
            resp = send_request(_url)
            soup = bs4.BeautifulSoup(resp.content, 'html.parser')
            init()
            print_soup(soup)
            deinit()
            save_webpage(_url, soup)
        else:
            print_file(_url)
    elif check_File(_url):
        print_file(_url)
    else:
        print("Error: Incorrect URL")


create_dir(dirName)
stack = deque()


def main():
    # init Colorama
    # init()
    url = ''

    # create_dir(dirName)
    # stack = deque()

    while url != 'exit':

        url = input("Enter Url: ")
        # url = input()
        if not url == 'exit':
            if not url == 'back':
                gotoWebsite(url)
                stack.append(url)
            else:
                # print(f" stack length : {len(stack)}")
                if len(stack) > 0:
                    stack.pop()
                if len(stack) > 0:
                    url = stack.pop()
                    # print(f" url: {url}")
                    gotoWebsite(url)
                else:
                    print('')


if __name__ == "__main__":
    main()
