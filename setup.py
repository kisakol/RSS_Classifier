from setuptools import setup, find_packages

setup(
    name='rssclassifier',
    version='0.1',
    author='Batuhan Kisakol',
    author_email='batuhankisakol@gmail.com',
    url='https://github.com/kisakol/RSS_Classifier',
    packages=find_packages(),
    package_data={
        'my_package': ['data/gene_modules/*.txt', 'data/model/*'],
    },
    install_requires=[
        'numpy==1.21.0',
        'pandas==1.2.1',
        'scikit-learn==0.24.2',
        'xgboost==1.4.2',
    ],
)