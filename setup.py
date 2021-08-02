import setuptools

with open("README.md", "r") as fil:
    long_description = fil.read()
with open("requirements.txt", "r") as fil:
    requirements = [line.strip() for line in fil]

setuptools.setup(
    name="mediafile_renamator",
    version="0.0.1",
    author="Filip Klopec",
    author_email="filipklopec@gmail.com",
    description="Mediafile Renamator is an application for renaming media files like movies, TV shows and music.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)
