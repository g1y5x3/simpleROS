from setuptools import setup

setup(
    capnpy_schemas=[
        "simpleros/msg/std_msg.capnp",
        "simpleros/msg/geometry_msg.capnp",
    ],
    capnpy_options={
        "pyx": False,
        "convert_case": False,
        "text_type": "unicode",
    },
)
