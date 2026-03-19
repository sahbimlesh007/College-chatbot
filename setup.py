from setuptools import setup, find_packages

setup(
    name="collbot",
    version="0.1.0",
    author="Bimlesh Sah",
    description="College chatbot using OpenAI",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
)