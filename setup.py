from setuptools import setup

setup(
    name='spot_agent',
    version='0.1',
    description='',
    url='',
    packages=['spot_agent'],
    license='',
    author='Botond Barta',
    python_requires='',
    install_requires=[
        'ai2thor==5.0.0',
        'dotmap==1.3.30',
        'langchain==0.3.25',
        'langchain-ollama==0.3.3',
        'langchain-core==0.3.63',
        'langgraph==0.4.7',
        'requests==2.32.3',
        'setuptools==78.1.0',
    ]
)
