from setuptools import setup, find_packages

setup(
    name='sci_mplstyle_package',  # Replace with your package name
    version='0.1',
    packages=find_packages(),
    include_package_data=True,  # Ensures that non-Python files are included
    package_data={
        'sci_mplstyle_package': ['style_files/*.mplstyle'],  # Include the .mplstyle file
    },
    install_requires=[
        'matplotlib',  # Ensure matplotlib is installed as a dependency
    ],
    description='A package for custom matplotlib styles',
    author='Suparno Bhattacharyya',  # Replace with your name
    author_email='suparno.pa@gmail.com',  # Replace with your email
    url='https://github.com/suparnob100/sci_mplstyle_package',  # Replace with your repo URL if applicable
)
