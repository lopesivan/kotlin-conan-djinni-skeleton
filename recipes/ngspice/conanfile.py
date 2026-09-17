import os
import platform

from conan import ConanFile
from conan.errors import ConanException
from conan.tools.env import Environment
from conan.tools.files import copy, unzip
from conan.tools.layout import basic_layout


class NgspiceConan(ConanFile):
    name = "ngspice"
    version = "47"
    license = "BSD-3-Clause"
    url = "https://ngspice.sourceforge.io/"
    description = "ngspice 47 shared library for Android"
    package_type = "shared-library"

    settings = "os", "arch", "compiler", "build_type"

    def export_sources(self):
        source = os.path.normpath(
            os.path.join(self.recipe_folder, "..", "..", "third_party", "ngspice")
        )
        copy(
            self,
            "ngspice-47.tar.gz",
            src=source,
            dst=self.export_sources_folder,
        )

    def layout(self):
        basic_layout(self, src_folder="src")

    def source(self):
        unzip(
            self,
            os.path.join(self.export_sources_folder, "ngspice-47.tar.gz"),
            destination=self.source_folder,
            strip_root=True,
        )

    def _ndk_prebuilt(self):
        ndk = self.conf.get("tools.android:ndk_path")

        if not ndk:
            raise ConanException(
                "tools.android:ndk_path must point at Android NDK"
            )

        if platform.system() == "Linux":
            host = "linux-x86_64"
        elif platform.system() == "Windows":
            host = "windows-x86_64"
        else:
            host = "darwin-x86_64"

        return os.path.join(ndk, "toolchains", "llvm", "prebuilt", host)

    def _android_target(self):
        # Keep this aligned with third_party/ngspice/build-ngspice-android.sh.
        api = "35"
        arch = str(self.settings.arch)

        targets = {
            "armv8": ("aarch64-linux-android", f"aarch64-linux-android{api}"),
            "armv7": (
                "armv7a-linux-androideabi",
                f"armv7a-linux-androideabi{api}",
            ),
            "x86_64": ("x86_64-linux-android", f"x86_64-linux-android{api}"),
            "x86": ("i686-linux-android", f"i686-linux-android{api}"),
        }

        if arch not in targets:
            raise ConanException(f"unsupported Android arch {arch}")

        return targets[arch]

    def build(self):
        if self.settings.os != "Android":
            raise ConanException("this recipe only cross-compiles for Android")

        prebuilt = self._ndk_prebuilt()
        bindir = os.path.join(prebuilt, "bin")
        host, compiler_target = self._android_target()

        env = Environment()
        env.define("CC", os.path.join(bindir, f"{compiler_target}-clang"))
        env.define("CXX", os.path.join(bindir, f"{compiler_target}-clang++"))
        env.define("AR", os.path.join(bindir, "llvm-ar"))
        env.define("AS", os.path.join(bindir, f"{compiler_target}-clang"))
        env.define("LD", os.path.join(bindir, "ld.lld"))
        env.define("NM", os.path.join(bindir, "llvm-nm"))
        env.define("RANLIB", os.path.join(bindir, "llvm-ranlib"))
        env.define("STRIP", os.path.join(bindir, "llvm-strip"))
        env.define("CFLAGS", "-fPIC -O2")
        env.define("CXXFLAGS", "-fPIC -O2")
        env.define("CPPFLAGS", "-DHAVE_LIBPTHREAD=1")
        env.define("LDFLAGS", "-fPIC")
        env.define("LIBS", "-lm")
        env.define("ac_cv_func_malloc_0_nonnull", "yes")
        env.define("ac_cv_func_realloc_0_nonnull", "yes")
        env.define("ac_cv_lib_pthread_pthread_mutex_lock", "yes")
        env.define("ac_cv_func_getpwent", "no")
        env.define("ac_cv_func_setpwent", "no")
        env.define("ac_cv_func_endpwent", "no")

        # Android libraries must not use the desktop libtool SONAME
        # libngspice.so.0. Generate an unversioned libngspice.so instead.
        self.run(
            "sed -i -E "
            "'s/-version-info[[:space:]]+[^[:space:]]+/-avoid-version/g' "
            "src/Makefile.am",
            cwd=self.source_folder,
        )
        self.run("./autogen.sh", cwd=self.source_folder)

        configure = os.path.join(self.source_folder, "configure")
        args = [
            configure,
            f"--host={host}",
            "--prefix=/",
            "--with-ngshared",
            "--disable-openmp",
            "--disable-xspice",
            "--disable-debug",
            "--disable-static",
            "--enable-shared",
            "--without-x",
            "--without-readline",
        ]

        with env.vars(self).apply():
            self.run(" ".join(args), cwd=self.build_folder)
            jobs = self.conf.get("tools.build:jobs") or os.cpu_count() or 4
            self.run(f"make -j{jobs}", cwd=self.build_folder)

    def package(self):
        self.run(
            f"make install DESTDIR='{self.package_folder}'",
            cwd=self.build_folder,
        )
        copy(
            self,
            "COPYING",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses"),
        )

    def package_info(self):
        self.cpp_info.libs = ["ngspice"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.set_property("cmake_file_name", "ngspice")
        self.cpp_info.set_property(
            "cmake_target_name",
            "ngspice::ngspice",
        )

        if self.settings.os == "Android":
            self.cpp_info.system_libs.extend(["dl", "m"])
