from setuptools import setup, find_packages
from setuptools_rust import Binding, RustExtension


with open('requirements.txt', 'r')  as f:
	pkg_install = f.read().split()

setup(
	name='instagram_scrape',
	version='0.0.1',
	packages=['similarity_rs', 'pycode'],
	install_requires=pkg_install,
	rust_extensions =[RustExtension("similarity_rs.similarity_rs")],
	include_package_data=True,
	zip_safe=False,
)
