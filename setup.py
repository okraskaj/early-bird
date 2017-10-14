import os

from itertools import chain

from setuptools import (
    find_packages,
    setup,
)


def get_install_requires_list(requirements_path):
    """Return list of packages from the requirements file.
    """
    requirements_dir = 'requirements/'
    requirements = list()
    with open(requirements_path) as f:
        for line in f.readlines():
            if line.startswith('-r'):
                rpath = line.split(' ')[-1].strip()
                if not rpath.startswith(requirements_dir):
                    rpath = os.path.join(requirements_dir, rpath)
                requirements = chain(
                    requirements,
                    get_install_requires_list(rpath),
                )
            else:
                requirements.append(line)
    return list(set(requirements))


setup(
    name='app',
    version='0.0.1',
    packages=find_packages(include=('app*',)),
    include_package_data=True,
    install_requires=get_install_requires_list('requirements.txt'),
    zip_safe=False,
)
