load("@rules_python//python:py_binary.bzl", "py_binary")
load("@rules_python//python:py_library.bzl", "py_library")

package(
    default_visibility=["//visibility:public"],
)

py_binary(
    name = "dialog_parser",
    srcs = ["dialog_parser.py"],
    data = ["geneforge_filepaths.json"],
    deps = [
        "//src/objects:talk_node",
    ]
)

py_library(
    name = "scen_data_parser",
    srcs = ["scen_data_parser.py"],
    deps = [
    ]
)

py_library(
    name = "template_parser",
    srcs = ["template_parser.py"],
    deps = [
        "//src:gf_constants"
    ]
)
