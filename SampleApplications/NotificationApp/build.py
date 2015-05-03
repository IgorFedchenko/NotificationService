import sys, subprocess

subprocess.call("{0} assemble{1}".format(sys.argv[1], sys.argv[2]), cwd=sys.argv[3])