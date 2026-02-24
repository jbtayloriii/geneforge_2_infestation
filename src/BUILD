load("@rules_python//python:py_binary.bzl", "py_binary")
load("@rules_python//python:py_library.bzl", "py_library")

package(
    default_visibility=["//visibility:public"],
)

py_library(
    name = "gf_constants",
    srcs = ["gf_constants.py"],
)

py_binary(
    name = "parse_files",
    srcs = ["parse_files.py"],
    data = [
        "file_locations.json",
    ],
    deps = [
        ":gf_constants",
        "@abseil//absl:app",
        "@abseil//absl/flags",
        "//src/parsers:dialog_parser",
        "//src/parsers:scen_data_parser",
        "//src/parsers:template_parser",
    ]
)
