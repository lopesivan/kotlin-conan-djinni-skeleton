from conan import ConanFile
from conan.errors import ConanException
from conan.tools.files import copy, get
from conan.tools.layout import basic_layout
import os
import platform


class FfmpegAndroidConan(ConanFile):
    name = "ffmpeg"
    version = "8.1.2"
    license = "LGPL-2.1-or-later"
    url = "https://ffmpeg.org"
    description = "Reduced LGPL FFmpeg 8.1.2 built with the Android NDK triple compilers"
    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"

    def layout(self):
        basic_layout(self, src_folder="src")

    def source(self):
        get(
            self,
            "https://ffmpeg.org/releases/ffmpeg-8.1.2.tar.xz",
            sha256="464beb5e7bf0c311e68b45ae2f04e9cc2af88851abb4082231742a74d97b524c",
            strip_root=True,
        )

    def _ndk_prebuilt(self):
        ndk = self.conf.get("tools.android:ndk_path")
        if not ndk:
            raise ConanException("tools.android:ndk_path must point at NDK 29.0.14206865")
        host = "linux-x86_64" if platform.system() == "Linux" else "windows-x86_64"
        return os.path.join(ndk, "toolchains", "llvm", "prebuilt", host)

    def _android_triple(self):
        api = str(self.settings.os.api_level) if self.settings.os.api_level else "24"
        arch = str(self.settings.arch)
        if arch in ("armv8", "armv8.3"):
            return "aarch64", f"aarch64-linux-android{api}"
        if arch == "armv7":
            return "arm", f"armv7a-linux-androideabi{api}"
        if arch == "x86_64":
            return "x86_64", f"x86_64-linux-android{api}"
        if arch == "x86":
            return "x86", f"i686-linux-android{api}"
        raise ConanException(f"unsupported Android arch {arch}")

    def build(self):
        if self.settings.os != "Android":
            raise ConanException("this recipe only cross-compiles for Android")
        prebuilt = self._ndk_prebuilt()
        bindir = os.path.join(prebuilt, "bin")
        ffmpeg_arch, triple = self._android_triple()
        cc = os.path.join(bindir, f"{triple}-clang")
        cxx = os.path.join(bindir, f"{triple}-clang++")
        configure = os.path.join(self.source_folder, "configure")
        args = [
            configure,
            "--enable-cross-compile",
            "--target-os=android",
            f"--arch={ffmpeg_arch}",
            f"--cc={cc}",
            f"--cxx={cxx}",
            f"--ar={os.path.join(bindir, 'llvm-ar')}",
            f"--nm={os.path.join(bindir, 'llvm-nm')}",
            f"--ranlib={os.path.join(bindir, 'llvm-ranlib')}",
            f"--strip={os.path.join(bindir, 'llvm-strip')}",
            f"--sysroot={os.path.join(prebuilt, 'sysroot')}",
            "--prefix=/",
            "--enable-static",
            "--disable-shared",
            "--enable-pic",
            "--disable-asm",
            "--disable-doc",
            "--disable-programs",
            "--disable-autodetect",
            "--disable-network",
            "--disable-everything",
            "--disable-avdevice",
            "--disable-avfilter",
            "--disable-gpl",
            "--disable-nonfree",
            "--enable-avutil",
            "--enable-avcodec",
            "--enable-avformat",
            "--enable-swscale",
            "--enable-swresample",
            "--enable-protocol=file",
            "--enable-demuxer=yuv4mpegpipe",
            "--enable-decoder=rawvideo",
            "--extra-cflags=-fPIC",
        ]
        if self.settings.build_type == "Debug":
            args.extend(["--disable-optimizations", "--enable-debug", "--disable-stripping"])
        self.run(" ".join(f"'{part}'" if " " in part else part for part in args))
        jobs = self.conf.get("tools.build:jobs") or os.cpu_count() or 4
        self.run(f"make -j{jobs}")

    def package(self):
        self.run(f"make install DESTDIR='{self.package_folder}'")
        copy(self, "COPYING.LGPLv2.1", src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "LICENSE.md", src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "ffmpeg")
        self.cpp_info.set_property("cmake_target_name", "ffmpeg::ffmpeg")
        self.cpp_info.includedirs = ["include"]
        order = ["avformat", "avcodec", "swscale", "swresample", "avutil"]
        requires = {
            "avformat": ["avcodec", "avutil"],
            "avcodec": ["avutil", "swresample"],
            "swscale": ["avutil"],
            "swresample": ["avutil"],
            "avutil": [],
        }
        for name in order:
            component = self.cpp_info.components[name]
            component.libs = [name]
            component.set_property("cmake_target_name", f"ffmpeg::{name}")
            component.requires = requires[name]
            if self.settings.os == "Android":
                component.system_libs.extend(["m", "z", "android"])
        if self.settings.os == "Android":
            self.cpp_info.system_libs.extend(["m", "z", "android"])
