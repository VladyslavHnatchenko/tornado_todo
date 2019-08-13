from setuptools import setup, find_packages


requires = [
    "tornado",
    "tornado-sqlalchemy",
    "psycopg2",
]

setup(
    name="tornado_todo",
    version="0.1",
    description="To-Do List built with Tornado",
    author="",
    author_email="",
    keywords="web tornado",
    packages=find_packages(),
    install_requires=(),
    entry_points={
        "console_scripts": [
            "serve_app = todo:main",
        ],
    },
)
