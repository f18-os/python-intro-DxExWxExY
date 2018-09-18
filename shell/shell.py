#!/usr/bin/env python3

import os, sys, time, re, getpass, subprocess

def fork_process(program_args):
	if 'cd' in program_args:
		try:
			os.chdir(program_args[1] + "/")
			return
		except Exception as e:
			os.chdir('/home/%s' % getpass.getuser())
			return
	else:
		rc = os.fork()
		if rc < 0: # fork failed
			os.write(2, "Fork Failed. Exiting...".encode())
			sys.exit(1)
		elif rc == 0: #fork child
			if '>' in program_args:
				redirect_output(program_args)
			elif '<' in program_args:
				redirect_input(program_args)
			elif '|' in program_args:
				pipe_program(program_args)
			else:
				execute_program(program_args)
		else: # fork parent
			os.wait()

def redirect_output(program_args):
	args = program_args[0 : program_args.index('>')]
	out_file = program_args[program_args.index('>') + 1 : ]
	os.close(1)                 # redirect child's stdout
	sys.stdout = open(out_file[0], "w")
	fd = sys.stdout.fileno()
	os.set_inheritable(fd, True)
	execute_program(args)

def redirect_input(program_args):
	args = program_args[0 : program_args.index('<')]
	in_args = program_args[program_args.index('<') + 1 : ]
	os.close(0)
	sys.stdin = open(in_args[0], "r")
	fd = sys.stdin.fileno()
	os.set_inheritable(fd, True)
	execute_program(args)
		
def pipe_program(program_args):
	left = program_args[0 : program_args.index('|')]
	right = program_args[program_args.index('|') + 1 : ]
	pc = os.fork()
	if pc == 0:
		os.close(1)
		sys.stdout = open('pipe','w')
		fd = sys.stdout.fileno()
		os.set_inheritable(fd, True)
		execute_program(left)
	else:
		os.wait()
		os.close(0)
		sys.stdin = open('pipe', 'r')
		fd = sys.stdin.fileno()
		os.set_inheritable(fd, True)
		execute_program(right)

def execute_program(args):
	try:
		subprocess.call(args)
	except Exception as e:
		for dir in re.split(":", os.environ['PATH']): 
			program = "%s/%s" % (dir, args[0])
			try:
				os.execve(program, args, os.environ)
			except FileNotFoundError:
				pass
		os.write(2, ("Program Not Found. %s \n" % e).encode())
		sys.exit(1)
	finally:
		sys.exit(0)

if __name__ == '__main__':
	user_input = ['clear']
	while not 'exit' in user_input:
		if not user_input is ['']:
			fork_process(user_input)
		# os.write(1, "\nshell\n>".encode())
		# user_input = os.read(0, 50).decode().strip().split(' ')
		user_input = input().split('')
	sys.exit(0)