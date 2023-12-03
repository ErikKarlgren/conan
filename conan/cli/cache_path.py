from conan.api.conan_api import ConanAPI
from conan.errors import ConanException
from conans.model.package_ref import PkgReference
from conans.model.recipe_ref import RecipeReference


def get_cache_path(conan_api: ConanAPI, reference, folder) -> str:
    """
    Get the corresponding path to a reference's folder
    """
    try:
        pref = PkgReference.loads(reference)
    except ConanException:
        pref = None

    if not pref:  # Not a package reference
        ref = RecipeReference.loads(reference)
        if folder is None:
            path = conan_api.cache.export_path(ref)

        elif folder == "export_source":
            path = conan_api.cache.export_source_path(ref)
        elif folder == "source":
            path = conan_api.cache.source_path(ref)
        elif folder == "metadata":
            path = conan_api.cache.recipe_metadata_path(ref)
        else:
            raise ConanException(
                f"'--folder {folder}' requires a valid package reference"
            )
    else:
        if folder is None:
            path = conan_api.cache.package_path(pref)
        elif folder == "build":
            path = conan_api.cache.build_path(pref)
        elif folder == "metadata":
            path = conan_api.cache.package_metadata_path(pref)
        else:
            raise ConanException(f"'--folder {folder}' requires a recipe reference")

    return path
