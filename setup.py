import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MachineDesktopInterface", # Replace with your own username
    version="0.2.4",
    author="Breeana Proffit",
    author_email="author@example.com",
    description="A tool to allow machine learning developers to interact with applications on their comptuers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BreeanaProffit/MachineDesktopInterface",
    packages=setuptools.find_packages(),
    install_requires=['mss','numpy','pyautogui','pygetwindow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)