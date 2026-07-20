from setuptools import setup, find_packages

setup(
    name='s-voice-whisper',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask==2.3.2',
        'flask-cors==4.0.0',
        'openai-whisper',
        'torch==2.0.1',
        'soundfile==0.12.1',
        'numpy==1.24.3',
    ],
)
