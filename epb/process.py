# [Back to blast.py](blast.html)

import os
from os import path
import shlex
import subprocess
from subprocess import PIPE

# === run ===
#
# **Takes:** `command` to run, `input` to pass on stdin
#
# **Returns:** `output` from stdout
def run(command, input):
	command = shlex.split(command)
	
	if not which(command[0]):
		raise ExecutableNotFound("can't find '%s' executable in PATH" % command)
	
	p = subprocess.Popen(
		command, stdin=PIPE, stdout=PIPE, stderr=PIPE
	)
	
	output, err = p.communicate(input)
	if p.returncode != 0:
		raise ProcessFailed(
			"Return code %i from '%s'\n%s\n%s" % (p.returncode, command, output, err)
		)
	return output

# Does the command exist in our path?
def which(command):
	bin = os.environ['PATH'].split(os.pathsep)
	return any(path.exists(path.join(p, command)) for p in bin)

# === ExecutableNotFound ===
class ExecutableNotFound(Exception): pass
# === ProcessFailed ===
class ProcessFailed(Exception): pass