load("@rules_python//python:py_binary.bzl", "py_binary")

py_binary(
    name = "parse_files",
    srcs = ["parse_files.py"],
    data = [
        "file_locations.json",
    ],
    deps = [
        "@abseil//absl:app",
        "@abseil//absl/flags",
        "//src/parsers:dialog_parser",
        "//src/parsers:scen_data_parser",
    ]
)
