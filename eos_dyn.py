#!/usr/bin/env python3
import re
import sys
import subprocess
import os

my_dir=os.getcwd()
my_env=os.environ.copy()

file_list=os.listdir(my_dir)

list=[]
for f in file_list:
	if f != "eos_dyn.py":
		list.append(f)
dict={}
for f in list:
	with open(f) as r:
		reader=r.read()
	dict[f]=reader

for i in [-20, -60, -100, -140, 20, 60, 100, 140,200, 300]:
	os.mkdir("press_{}".format(i))
	my_new_dir=os.path.join(my_dir,"press_{}".format(i))
	os.chdir(my_new_dir)
	for k,v in dict.items():
		with open(k,"w") as w:
			w.write(v)
	with open("sto99.in") as r:
		lines=r.readlines()
	new_lines = []
	for line in lines:
		if "calculation" in line:
			line = "  calculation = 'vc-relax'\n"
		new_lines.append(line)
	for n,l in enumerate(new_lines):
		if "mixing_beta" in l:
			head=new_lines[:n+2]
			medium=["&IONS\n","  ion_dynamics ='bfgs'\n","/\n","&CELL\n","  cell_dynamics = 'bfgs'\n","  press = {}\n".format(i),"/\n"]
			tail=new_lines[n+2:]
	newlines=head+medium+tail
	with open("sto.vc-relax.in","w") as w:
		w.writelines(newlines)
	os.chdir(my_dir)



def process(input, output):         # function to execute pw.x calculation on prepared scf or nscf files           
	pw ="#!/bin/bash\nmpirun -np 6 ~/Téléchargements/qe-6.8/bin/pw.x -i {} > {}".format(input,output) #pw ="#!/bin/bash\nmpirun  -np $SLURM_NTASKS pw.x -i {} > {}".format(input,output)
	with open("run.sh","w") as w:
		w.write(pw)
	subprocess.run(["chmod","+x","run.sh"])
	subprocess.run(["./run.sh"])
	os.remove("run.sh")

for i in [-20, -60, -100, -140, 20, 60, 100, 140,200, 300]:
	my_new_dir=os.path.join(my_dir,"press_{}".format(i))
	os.chdir(my_new_dir)
	process("sto.vc-relax.in","sto.vc-relax.out")
	os.chdir(my_dir)
