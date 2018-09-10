import os, sys, time, re

def fork_process(program_args):
	rc = os.fork()
	if rc < 0: # fork failed
		os.write(1, "Fork Failed. Exiting...".encode())
		sys.exit(1)
	elif rc == 0: #fork child
		if '>' in program_args:
			args = program_args[0 : program_args.index('>')]
			out_file = program_args[program_args.index('>') + 1 : ]
			os.close(1)                 # redirect child's stdout
			sys.stdout = open(out_file[0], "w")
			fd = sys.stdout.fileno()
			os.set_inheritable(fd, True)
			execute_program(args)
		elif '<' in program_args:
			args = program_args[0 : program_args.index('<')]
			in_args = program_args[program_args.index('<') + 1 : ]
			# os.close(1)
			# args.append("temp.txt")
			# sys.stdout = open('temp.txt', "w")
			# fd = sys.stdout.fileno()
			# os.set_inheritable(fd, True)
			# fork_process(in_args)
			# os.wait
			execute_program(args)
		else:
			execute_program(program_args)
	else: # fork parent
		os.wait()

def execute_program(args):
	for dir in re.split(":", os.environ['PATH']): 
		program = "%s/%s" % (dir, args[0])
		try:
			os.execve(program, args, os.environ)
		except FileNotFoundError:
			pass
	os.write(2, "Program Not Found.\n".encode())
	sys.exit(1)

if __name__ == '__main__':
	user_input = ['clear']
	while not 'q' in user_input:
		fork_process(user_input)
		user_input = input("Program to Run. \'q \' to Quit: ").split(' ')
	sys.exit(1)