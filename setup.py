from setuptools import setup, find_packages

setup(
    name="encrypt",
    version="0.1",
    packages=find_packages(),
    description="encrypt",
    long_description="encrypt",
    author="clvsit",
    author_email="879646529@qq.com",

    license="GPL",
    keywords=["encrypt", "code secret"],
    platforms="Independant",
    url="https://cnblog.com",
    entry_points={
        "console_scripts": [
            "encrypt = encrypt.main:main",
        ]
    }
)
