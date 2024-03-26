from setuptools import setup, find_packages

setup(
    name='RSS_Classifier',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy==1.21.0',
        'pandas==1.2.1',
        'scikit-learn==0.24.2',
        'xgboost==1.4.2',
    ],
)