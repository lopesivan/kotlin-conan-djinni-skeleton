import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy


class BodenLoggerConan(ConanFile):
    name = "boden-logger"
    version = "0.1.0"
    package_type = "static-library"
    license = "MIT"
    description = "Thread-safe extensible C++ logger for Boden applications"
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    generators = "CMakeDeps"

    def export_sources(self):
        copy(
            self,
            "*",
            src=os.path.join(
                self.recipe_folder, "..", "..", "modules", "logger"
            ),
            dst=self.export_sources_folder,
        )

    def requirements(self):
        self.requires("boden-datetime/0.1.0")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.variables["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.get_safe(
            "fPIC", True
        )
        toolchain.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=self.source_folder)
        cmake.build()

    def package(self):
        copy(
            self,
            "*.h",
            src=os.path.join(self.source_folder, "include"),
            dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*.a",
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            "*.lib",
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )

    def package_info(self):
        self.cpp_info.libs = ["boden_logger"]
        self.cpp_info.set_property("cmake_file_name", "boden-logger")
        self.cpp_info.set_property("cmake_target_name", "boden::logger")
