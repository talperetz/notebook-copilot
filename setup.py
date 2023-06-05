from setuptools import setup, find_packages

setup(
    name='notebook_copilot',
    version='0.1.1',
    packages=find_packages(),
    description='The Bridge from Thoughts to Well-Crafted Jupyter Notebook',
    install_requires=[
        'setuptools~=65.5.1',
        'ipython~=8.13.2',
        'langchain~=0.0.187',
        'pandas~=2.0.2',
        'pydantic~=1.10.8',
        'tiktoken~=0.4.0',
        'faiss-cpu~=1.7.4'
    ],
    author="Tal Peretz",
    author_email="tp@aihumanlabs.com",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/talperetz/notebook_copilot",
    license="MIT",
)
