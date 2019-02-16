from setuptools import setup

def build_native(spec):
	# build an example rust library
	build = spec.add_external_build(
		cmd=['cargo', 'build', '--release'],
		path='./rust'
	)

	spec.add_cffi_module(
		module_path='python._native',
		dylib=lambda: build.find_dylib('python', in_path='target/release'),
		header_filename=lambda: build.find_header('python.h', in_path='target'),
		rtld_flags=['NOW', 'NODELETE']
	)

setup(
	name='python',
	version='0.0.1',
	packages=['python'],
	zip_safe=False,
	platforms='any',
	setup_requires=['milksnake'],
	install_requires=['milksnake', 'numpy', 'pymysql', 'networkx', 'selenium'],
	milksnake_tasks=[
		build_native
	]
)
