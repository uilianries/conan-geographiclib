#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GeographiclibConan(ConanFile):
    name = "GeographicLib"
    version = "1.49"
    description = "Convert geographic units and solve geodesic problems"
    url = "https://github.com/bincrafters/conan-geographiclib"
    homepage = "https://geographiclib.sourceforge.io/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.txt"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://git.code.sf.net/p/geographiclib/code"
        tools.download("{0}/{1}-{2}.tar.gz/download".format(
            "https://sourceforge.net/projects/geographiclib/files/distrib",
            self.name,
            self.version),
            filename="{0}-{1}.tar.gz".format(self.name, self.version)
        )

        tools.unzip("GeographicLib-{0}.tar.gz".format(self.version))
        extracted_dir = self.name + "-" + self.version

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False # example
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        if self.options.shared:
            cmake.definitions['GEOGRAPHICLIB_LIB_TYPE'] = 'SHARED'
        else:
            cmake.definitions['GEOGRAPHICLIB_LIB_TYPE'] = 'STATIC'
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
