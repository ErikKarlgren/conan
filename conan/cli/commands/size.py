# -*- coding: utf-8 -*-
from conan.api.conan_api import ConanAPI
from conan.cli.command import conan_command
from conan.cli.cache_path import get_cache_path


@conan_command(group="Consumer")
def size(conan_api: ConanAPI, parser, *args):
    """
    Display the size of the artifacts in a package, and the total size
    """
    parser.add_argument("reference", help="Recipe reference or Package reference")
    parser.add_argument(
        "--folder",
        choices=["export_source", "source", "build", "metadata"],
        help="Path to show. The 'build' requires a package reference. "
        "If the argument is not passed, it shows 'exports' path for recipe references "
        "and 'package' folder for package references.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show the size of all artifacts"
    )
    parser.add_argument(
        "--in-bytes",
        action="store_true",
        help="Show the size in bytes instead of the most appropiate unit in each "
        "case (B, KB, MB, ...)",
    )

    args = parser.parse_args(*args)
    path = get_cache_path(conan_api, args.reference, args.folder)
    conan_api.size.directory_total_size(path, args.verbose, args.in_bytes)
