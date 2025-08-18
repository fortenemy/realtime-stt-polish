#!/usr/bin/env python3
"""
Setup script for Real-time Speech-to-Text Polish
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="realtime-stt-polish",
    version="0.1.0",
    author="Real-time STT Team",
    author_email="contact@realtime-stt-polish.com",
    description="Real-time Speech-to-Text system optimized for Polish language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/realtime-stt-polish",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/realtime-stt-polish/issues",
        "Documentation": "https://github.com/your-username/realtime-stt-polish/wiki",
        "Source Code": "https://github.com/your-username/realtime-stt-polish",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
        "full": [
            "openai-whisper>=20231117",
            "torch>=2.0.0",
            "webrtcvad>=2.0.10",
        ],
    },
    entry_points={
        "console_scripts": [
            "realtime-stt=main:main",
        ],
    },
    keywords=[
        "speech-to-text",
        "real-time",
        "polish",
        "voice-recognition",
        "audio-processing",
        "whisper",
        "vad",
        "transcription",
    ],
    include_package_data=True,
    zip_safe=False,
)
