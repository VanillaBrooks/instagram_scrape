import subprocess
import sys
from setuptools import setup, find_packages


print('\n\n\n\n IN NESTED \n\n\n\n')

try:
	from setuptools_rust import RustExtension
except ImportError:

	errno = subprocess.call([sys.executable, "-m", "pip", "install", "setuptools-rust"])
	if errno:
		print("Please install setuptools-rust package")
		raise SystemExit(errno)
	else:
		from setuptools_rust import RustExtension


# this is main directory

with open('requirements.txt', 'r')  as f:
	pkg_install = f.read().split()



setup(
	name='similarity_rs',
	version='0.0.1',
	packages=['pycode', 'rust'],
	install_requires=pkg_install,
	include_package_data=True,
	zip_safe=False,
)

# subprocess([sys.executable, '/rust/setup.py', 'install'])
		# [sys.executable, "-m", "pip", "install", "setuptools-rust"]
subprocess.Popen(['python','setup.py', 'install'], cwd='rust')
