# coding: utf-8

from setuptools import setup


setup(name='pyquality',
      version='0.1.0',
      author=('Álvaro Justen <alvarojusten@gmail.com>',
              'Flávio Amieiro <flavioamieiro@gmail.com>'),
      author_email='alvarojusten@gmail.com',
      url='https://github.com/NAMD/pyquality',
      description='Rich reports for Python code quality',
      entry_points={'console_scripts': ['pyquality = pyquality.cli:main']},
      packages=['pyquality'],
      install_requires=['flake8', 'numpy', 'requests', 'matplotlib>=1.3.0',
                        'strobo', 'jinja2'],
      license='GPL',
      zip_safe=False,
      keywords=['code quality', 'pep8'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
