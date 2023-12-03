from conan.api.conan_api import ConanAPI
from conan.cli.command import conan_command
from conan.errors import ConanException
from conans.model.package_ref import PkgReference
from conans.model.recipe_ref import RecipeReference


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
    try:
        pref = PkgReference.loads(args.reference)
    except ConanException:
        pref = None

    if not pref:  # Not a package reference
        ref = RecipeReference.loads(args.reference)
        if args.folder is None:
            path = conan_api.cache.export_path(ref)

        elif args.folder == "export_source":
            path = conan_api.cache.export_source_path(ref)
        elif args.folder == "source":
            path = conan_api.cache.source_path(ref)
        elif args.folder == "metadata":
            path = conan_api.cache.recipe_metadata_path(ref)
        else:
            raise ConanException(
                f"'--folder {args.folder}' requires a valid package reference"
            )
    else:
        if args.folder is None:
            path = conan_api.cache.package_path(pref)
        elif args.folder == "build":
            path = conan_api.cache.build_path(pref)
        elif args.folder == "metadata":
            path = conan_api.cache.package_metadata_path(pref)
        else:
            raise ConanException(
                f"'--folder {args.folder}' requires a recipe reference"
            )
    conan_api.size.directory_total_size(path, args.verbose, args.in_bytes)
