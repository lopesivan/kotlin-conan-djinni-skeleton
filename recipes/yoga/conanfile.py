from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get
import os


class YogaConan(ConanFile):
    name = "yoga"
    version = "3.2.1"
    license = "MIT"
    url = "https://github.com/facebook/yoga"
    description = "Yoga 3.2.1 flexbox engine packaged for Android/NDK reuse"
    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    implements = ["auto_shared_fpic"]

    def source(self):
        get(
            self,
            "https://github.com/facebook/yoga/archive/refs/tags/v3.2.1.tar.gz",
            strip_root=True,
        )

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["YOGA_BUILD_TESTS"] = False
        tc.cache_variables["CMAKE_CXX_STANDARD"] = "20"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build(target="yogacore")

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "*.h", src=os.path.join(self.source_folder, "yoga"),
             dst=os.path.join(self.package_folder, "include", "yoga"))
        copy(self, "libyogacore.a", src=os.path.join(self.build_folder, "yoga"),
             dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "libyogacore.a", src=self.build_folder,
             dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "yogacore.lib", src=self.build_folder,
             dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["yogacore"]
        self.cpp_info.set_property("cmake_file_name", "yoga")
        self.cpp_info.set_property("cmake_target_name", "yoga::yoga")
        self.cpp_info.includedirs = ["include"]
