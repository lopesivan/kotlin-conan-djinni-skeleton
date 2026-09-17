from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get
import os


class AllegroConan(ConanFile):
    name = "allegro"
    version = "5.2.11.3"
    license = "Zlib"
    url = "https://github.com/liballeg/allegro5"
    description = "Experimental Android Conan recipe for Allegro 5.2.11.3"
    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    implements = ["auto_shared_fpic"]

    def source(self):
        get(
            self,
            "https://github.com/liballeg/allegro5/archive/refs/tags/5.2.11.3.tar.gz",
            strip_root=True,
        )

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.cache_variables["SHARED"] = False
        tc.cache_variables["WANT_EXAMPLES"] = False
        tc.cache_variables["WANT_DEMO"] = False
        tc.cache_variables["WANT_TESTS"] = False
        tc.cache_variables["WANT_DOCS"] = False
        tc.cache_variables["WANT_IMAGE"] = False
        tc.cache_variables["WANT_AUDIO"] = False
        tc.cache_variables["WANT_FONT"] = False
        tc.cache_variables["WANT_TTF"] = False
        tc.cache_variables["WANT_PRIMITIVES"] = False
        tc.cache_variables["WANT_NATIVE_DIALOG"] = False
        tc.cache_variables["WANT_VIDEO"] = False
        tc.cache_variables["WANT_PHYSFS"] = False
        tc.cache_variables["WANT_PYTHON_WRAPPER"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        # Default ALL also builds the bundled Gradle AAR (JDK 8-era wrapper).
        cmake.build(target="allegro")

    def package(self):
        copy(self, "LICENSE.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))

        # Allegro's public headers include files from allegro5/inline/*.inl.
        # Copy the complete include trees so these required inline definitions
        # and the generated platform headers are present in the Conan package.
        copy(self, "*", src=os.path.join(self.source_folder, "include"),
             dst=os.path.join(self.package_folder, "include"))
        copy(self, "*", src=os.path.join(self.build_folder, "include"),
             dst=os.path.join(self.package_folder, "include"))

        copy(self, "liballegro*.a", src=os.path.join(self.build_folder, "lib"),
             dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "liballegro*.a", src=self.build_folder,
             dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        suffix = "-debug-static" if self.settings.build_type == "Debug" else "-static"
        self.cpp_info.libs = [f"allegro{suffix}"]
        self.cpp_info.defines.append("ALLEGRO_STATICLINK")
        self.cpp_info.set_property("cmake_file_name", "allegro")
        self.cpp_info.set_property("cmake_target_name", "allegro::allegro")
        if self.settings.os == "Android":
            self.cpp_info.system_libs.extend(["android", "log", "EGL", "GLESv2", "z"])
