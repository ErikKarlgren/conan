# -*- coding: utf-8 -*-
import os


class SizeAPI:
    def __init__(self, conan_api):
        self.conan_api = conan_api

    def directory_total_size(self, path: str, verbose: bool, in_bytes: bool):
        """
        Receives a path and prints the total size taken up by the files inside it.
        """
        if total_size := _calculate_total_size_bytes(path, verbose, in_bytes):
            print(_size_and_path_as_str(path, total_size, in_bytes))
        else:
            print(f"Empty folder\t{path}")


def _size_and_path_as_str(path, size, in_bytes: bool):
    if in_bytes:
        return f"{size} {path}"

    return f"{_format_size_in_bytes(size)} {path}"


def _format_size_in_bytes(size: int):
    all_units = ["B", "KB", "MB", "GB", "TB", "PB", "EX", "ZB", "YB"]
    multiplier = 1024
    number_of_conversions = 0

    while size >= multiplier:
        size /= multiplier
        number_of_conversions += 1

    max_width = 10  # i.e. sizes such as "1023.01 KB"
    return f"{size:.2f} {all_units[number_of_conversions]}".rjust(max_width)


def _calculate_total_size_bytes(path, verbose: bool, in_bytes: bool) -> int:
    size = 0
    for f in os.listdir(path):
        pathname = os.path.join(path, f)
        try:
            file_size = os.path.getsize(pathname)
            size += file_size

            if verbose:
                msg = _size_and_path_as_str(pathname, file_size, in_bytes)
                if not os.path.exists(pathname):
                    msg += f"broken symbolic link {pathname}"
                print(msg)

            if os.path.isdir(pathname):
                size += _calculate_total_size_bytes(pathname, verbose, in_bytes)
        except PermissionError:
            print(f"cannot access {pathname}")
    return size
