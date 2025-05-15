from setuptools import setup, find_packages
from pathlib import Path

README = Path('README.md').read_text()

setup(
    name='yt-transcript-clipper',
    version='0.1.0',
    description='Extract YouTube video transcripts and copy to clipboard',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/Sharma-IT/yt-transcript-clipper',
    author='Shubham Sharma',
    author_email='shubhamsharma.emails@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'youtube-transcript-api>=0.6.0',
        'pyperclip>=1.8.2',
        'requests>=2.28.0',
        'typer>=0.7.0',
        'rich>=13.0.0',
    ],
    entry_points={
        'console_scripts': [
            'yt-transcript-clipper=yt_transcript_clipper.cli:app',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)