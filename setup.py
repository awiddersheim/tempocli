import io

from setuptools import find_packages
from setuptools import setup


def local_scheme(version):
    from pkg_resources import iter_entry_points

    # NOTE(awiddersheim): Modify default behaviour slightly by not
    # adding any local scheme to a clean `main` branch.
    if version.branch == 'main' and not version.dirty:
        return ''

    for item in iter_entry_points(
        'setuptools_scm.local_scheme',
        'node-and-date',
    ):
        return item.load()(version)


with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='tempocli',
    use_scm_version={
        'git_describe_command': 'git describe --dirty --tags --long --match "v*.*" --exclude "*.dev*" --first-parent',
        'local_scheme': local_scheme,
        'write_to': 'tempocli/version.py',
    },
    setup_requires=[
        'setuptools_scm>=3.2.0',
    ],
    author='Andrew Widdersheim',
    author_email='amwiddersheim@gmail.com',
    url='https://github.com/awiddersheim/tempocli',
    description='Command line interface for interacting with Tempo.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'arrow',
        'click>=7',
        'pyyaml',
        'requests',
        'requests-futures>=0.9.9',
        'tqdm',
    ],
    extras_require={
        'dev': [
            'flake8',
            'flake8-bandit',
            'flake8-commas',
            'flake8-import-order',
            'flake8-import-single',
            'flake8-print',
            'flake8-quotes',
            'pytest',
            'pytest-click',
            'pytest-cov',
            'pytest-freezegun',
            'requests-mock',
        ],
    },
    entry_points={
        'console_scripts': [
            'tempocli=tempocli.cli:main',
        ],
    },
    zip_safe=False,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
