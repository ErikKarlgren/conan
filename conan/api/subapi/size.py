import os


class SizeAPI:
    def __init__(self, conan_api):
        self.conan_api = conan_api

    def directory_total_size(self, path: str, verbose: bool):
        """
        Receives a path and prints the total size taken up by the files inside it.
        """
        if total_size := _calculate_total_size_bytes(path, verbose):
            formatted_size = _format_size_in_bytes(total_size)
            print(f"{formatted_size}\t{path}")
        else:
            print(f"Empty folder\t{path}")


def _format_size_in_bytes(size: int):
    all_units = ["B", "KB", "MB", "GB", "TB", "PB", "EX", "ZB", "YB"]
    multiplier = 1024
    number_of_conversions = 0

    while size >= multiplier:
        size /= multiplier
        number_of_conversions += 1

    max_width = 10  # i.e. sizes such as "1023.01 KB"
    return f"{size:.2f} {all_units[number_of_conversions]}".rjust(max_width)


def _calculate_total_size_bytes(path, verbose) -> int:
    size = 0
    for f in os.listdir(path):
        pathname = os.path.join(path, f)
        try:
            file_size = os.path.getsize(pathname)
            if verbose:
                print(f"{_format_size_in_bytes(file_size)} \t{pathname}")
            size += file_size

            if not os.path.exists(pathname):
                if verbose:
                    print(f"broken symbolic link {pathname}")
            elif os.path.isdir(pathname):
                size += _calculate_total_size_bytes(pathname, verbose)
        except PermissionError:
            print(f"cannot access {pathname}")
    return size
