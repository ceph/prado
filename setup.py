from setuptools import setup, find_packages

setup(
    name='prado',
    version='0.1',
    description='',
    author='',
    author_email='',
    install_requires=[
        "pecan",
    ],
    test_suite='prado',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages()
)
