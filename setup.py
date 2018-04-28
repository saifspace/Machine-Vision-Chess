# from cx_Freeze import setup, Executable

# includeFiles = ["Libraries\\"]
# packages = ["numpy"]
# setup(name='test', version='1.0',options= {'build_exe': {'include_files': includeFiles, "packages":packages}} ,executables = [Executable('MainWindow.py')])

"""
hi
saif
"""

from cx_Freeze import setup, Executable
import os

setup(name='test', version='1.0',executables = [Executable('MVC.py')])

def test():
	"""
	yes
	:return:
	"""
	print('hello')