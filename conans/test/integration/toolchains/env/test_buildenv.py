import platform
import textwrap

import pytest

from conans.test.utils.tools import TestClient


@pytest.mark.skipif(platform.system() != "Windows", reason="Fails on windows")
def test_crossbuild_windows_incomplete():
    client = TestClient()
    conanfile = textwrap.dedent("""
        from conan import ConanFile
        from conan.tools.cmake import CMake
        class Pkg(ConanFile):
            name = "pkg"
            version = "0.1"
            settings = "os", "compiler", "build_type", "arch"
            generators = "CMakeToolchain"
            def build(self):
                self.run("dir c:")
            """)
    build_profile = textwrap.dedent("""
        [settings]
        arch=x86_64
    """)
    client.save({"conanfile.py": conanfile, "build_profile": build_profile})
    client.run("create . -pr:b=build_profile", assert_error=True)
    assert "ERROR: Error in generator 'CMakeToolchain': "\
           "The 'build' profile must have a 'os' declared" in client.out

    build_profile = textwrap.dedent("""
        [settings]
        os=Windows
        arch=x86_64
        """)
    client.save({"conanfile.py": conanfile, "build_profile": build_profile})
    client.run("create . -pr:b=build_profile")
    assert "<DIR>          ." in client.out
