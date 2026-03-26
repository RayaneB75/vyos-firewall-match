"""Setup configuration for VyFwMatch."""

from setuptools import find_packages, setup

setup(
    name="vyfwmatch",
    version="2.0.0",
    description="VyOS Firewall Policy Matcher",
    author="VyFwMatch Contributors",
    packages=find_packages(exclude=["tests", "tests.*", "vyos-1x", "vyos-1x.*"]),
    python_requires=">=3.10",
    install_requires=[
        "ipaddress",
        "jinja2>=3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pylint>=2.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vyfwmatch=vyfwmatch.main:main",
        ],
    },
)
