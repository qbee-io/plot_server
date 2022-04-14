from setuptools import setup #, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="http-plot-server",
    version="0.1",
    description="A simple and lightweight http server to visualize measurements",
    long_description=long_description,
    url="https://github.com/qbee-io/plot_server",
    long_description_content_type="text/markdown",
    author="qbee.io",
    author_email="pypi@qbee.io",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Customer Service",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: JavaScript",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Text Processing :: Markup :: HTML"
    ],
    keywords="plot server, visualization, plotly, http, measurements",
    #package_dir={"": "plot_server"},
    #packages=find_packages(where="plot_server"),
    package_data={
        "plot_server": ["plotly/minimal.html"],
    },
    packages=["plot_server"],
    python_requires=">=3.5, <4",
    install_requires=["python-dateutil"],
    include_package_data=True,
    license='MIT',
    #scripts=["bin/plot_server"],
    entry_points={
        'console_scripts': ['plot_server=plot_server.server_setup:main'],
    },
    project_urls={
        "qbee Homepage": "https://qbee.io/",
        "qbee Docs": "https://qbee.io/docs/",
        "Source": "https://github.com/qbee-io/plot_server",
    },
)
