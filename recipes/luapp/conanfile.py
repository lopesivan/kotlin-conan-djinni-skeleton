import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy


class LuappConan(ConanFile):
    name = "luapp"
    version = "5.3.6"
    package_type = "shared-library"

    settings = "os", "arch", "compiler", "build_type"

    def export_sources(self):
        luapp_source = os.path.normpath(
            os.path.join(self.recipe_folder, "..", "..", "third_party", "luapp")
        )
        copy(self, "CMakeLists.txt", src=luapp_source, dst=self.export_sources_folder)
        copy(
            self,
            "lua-5.3.6/*",
            src=luapp_source,
            dst=self.export_sources_folder,
        )

    def layout(self):
        cmake_layout(self)

    def generate(self):
        CMakeDeps(self).generate()
        toolchain = CMakeToolchain(self)
        toolchain.cache_variables["CMAKE_CXX_STANDARD"] = "20"
        toolchain.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["luapp5.3"]
        self.cpp_info.includedirs = ["include/luapp"]
        self.cpp_info.set_property("cmake_file_name", "luapp")
        self.cpp_info.set_property("cmake_target_name", "luapp::luapp")

        if self.settings.os == "Android":
            self.cpp_info.system_libs.extend(["dl", "log"])
        elif self.settings.os in ("Linux", "FreeBSD"):
            self.cpp_info.system_libs.append("dl")
