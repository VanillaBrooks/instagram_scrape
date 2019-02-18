from setuptools import setup, find_packages
from setuptools_rust import Binding, RustExtension


setup(
	name='similarity_rs',
	version='0.0.1',
	packages=['similarity_rs'],
	rust_extensions =[RustExtension("similarity_rs.similarity_rs")],
	include_package_data=True,
	zip_safe=False,
)
