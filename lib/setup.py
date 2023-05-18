from setuptools import setup


setup(
    name="spracket",
    version="0.1.0",
    py_modules=["cli"],
    install_requires=["click", "tabulate", "sqlalchemy"],
    entry_points={
        "console_scripts": [
            "sprackify = cli:welcome",
        ],
    },
)
