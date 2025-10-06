from setuptools import setup, find_packages

setup(
    name="verify-lawyer",
    version="1.0.0",
    description="Turkish Lawyer Verification CLI and Python Module",
    author="",
    packages=find_packages(),
    install_requires=[
        "browser-use",
        "playwright",
    ],
    entry_points={
        'console_scripts': [
            'verify-lawyer=verify_lawyer.cli:main',
        ],
    },
    python_requires='>=3.8',
)
