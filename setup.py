"""setup.py for kontrakto"""

import setuptools

setuptools.setup(
        name        = 'kontrakto', 
        version     = '0.1', 
        description = 'decorators for design-by-contract', 
        url         = 'https://github.com/lglassy/kontrakto',
        packages    = setuptools.find_packages('src'),
        package_dir = { 'kontrakto': 'src/kontrakto' }, 
	)

# end of file
