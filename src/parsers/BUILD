load("@rules_python//python:py_binary.bzl", "py_binary")

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
