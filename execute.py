#!/usr/bin/env python3
import re
import sys
import subprocess
import os

my_dir=os.getcwd()

with open("eos_dyn.py") as r:
	read_eos = r.read()


for i in [123, 129, 166, 221, 139, 225, 229] :  # 99
	os.chdir(os.path.join(my_dir,'sto{}'.format(i)))
	read_eos = re.sub(r'sto[\d]+.in','sto{}.in'.format(i), read_eos)
	with open("execute.py","w") as w:
		w.write(read_eos)
	subprocess.run(['chmod','+x','execute.py'])
	subprocess.run(['./execute.py'])
	os.chdir(my_dir)

