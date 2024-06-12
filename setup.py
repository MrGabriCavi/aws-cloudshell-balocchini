from setuptools import setup, find_packages

setup(
    name='aws_csh_balocchini',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'boto3>=1.18.0',
        'numpy>=1.20.1'
    ],
    extras_require={
        'dev': [
            'check-manifest',
            'coverage',
        ],
        'test': [
            'pytest',
            'pytest-cov',
        ],
    },
    entry_points={
        'console_scripts': [
            'aws-balocchini=balocchini.cli:main',
        ],
    },
    author='Gabriele Cavigiolo',
    author_email='gabri.cavi@gmail.com',
    description='Tools for cloudshell AWS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MrGabriCavi/aws-cloudshell-balocchini',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)