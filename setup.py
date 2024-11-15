from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name='intercept-it',
    version='0.0.1',
    author="Simon Shalnev",
    author_email="shalnev.sema@mail.ru",
    description="Generic exception handlers",
    long_description=readme,
    url="https://github.com/pro100broo/Intercept-it",
    keywords=["exceptions", "handler", "notifier"],
    packages=[
        'intercept_it',
        'intercept_it/utils',
        'intercept_it/loggers',
        'intercept_it/configs',
        'intercept_it/exceptions'],
    classifiers=[
        "Programming Language :: Python :: 3.7"
        "Programming Language :: Python :: 3.8"
        "Programming Language :: Python :: 3.9"
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries",
        "Typing :: Typed"
    ],
    install_requires=[
        "aiofiles>=24.1.0",
        "aiogram>=3.14.0",
        "aiohappyeyeballs>=2.4.3",
        "aiohttp<=3.9.0",
        "aiosignal>=1.3.1",
        "annotated-types>=0.7.0",
        "async-timeout>=4.0.3",
        "attrs>=24.2.0",
        "certifi>=2024.8.30",
        "colorama>=0.4.6",
        "frozenlist>=1.5.0",
        "idna>=3.10",
        "loguru>=0.7.2",
        "magic-filter>=1.0.12",
        "multidict>=6.1.0",
        "propcache>=0.2.0",
        "pydantic<2.10",
        "pydantic_core<=2.23.4",
        "python-dotenv>=1.0.1",
        "pytz>=2024.2",
        "typing_extensions>=4.12.2",
        "setuptools==75.5.0",
        "win32-setctime>=1.1.0",
        "yarl>=1.17.1"
    ],
)
