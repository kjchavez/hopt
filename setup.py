from setuptools import setup

setup(name='hopt',
      version=0.1,
      description='Hyperparameter search tool',
      author='Kevin Chavez',
      author_email='kevin.j.chavez@gmail.com',
      packages=['hopt'],
      entry_points={ 'console_scripts': ['hopt = hopt.__main__:main'] }
     )
