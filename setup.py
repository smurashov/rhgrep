import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    setup_requires=['pbr'],
    pbr=True,
    install_requires=required)
