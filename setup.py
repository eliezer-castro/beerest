from setuptools import setup, find_packages

setup(
  name="beerest",
  version="0.2.0",
  packages=find_packages(),
  install_requires=[
        'httpx',
        'dataclasses;python_version<"3.7"',
        'jsonpath-ng',
    ],
  author="eliezer-gino",
  author_email="eliezergino@gmail.com",
  description="A beerest é uma lib de testes de API que combina simplicidade, robustez e elegância, oferecendo uma experiência fluente de escrita de testes.",
  long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eliezer-castro/beerest",
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
  python_requires='>=3.12.1',
)