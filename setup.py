from setuptools import setup, find_packages

def build_native(spec):
	# build an example rust library
	build = spec.add_external_build(
		cmd=['cargo', 'build', '--release'],
		path='./rust'
	)

	spec.add_cffi_module(
		module_path='pycode._native',
		dylib=lambda: build.find_dylib('pycode', in_path='target/release'),
		header_filename=lambda: build.find_header('pycode.h', in_path='target'),
		rtld_flags=['NOW', 'NODELETE']
)


setup(
	name='pyrust code',
	version='0.0.1',
	packages=find_packages('.'),
	include_package_data=True,
	zip_safe=False,
	platforms='any',
<<<<<<< HEAD
	# install_requires=[
	# 	'milksnake',
	# ],
	# milksnake_tasks=[
	# 	build_native,
	# ]
=======
	install_requires=[
		'milksnake',
	],
	#milksnake_tasks=[
		#build_native,
	#]
>>>>>>> 4f43802791cbbbb266e0f9e70bb01a421269dd87
)
