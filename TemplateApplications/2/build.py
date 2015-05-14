import sys, subprocess, os

app_path = sys.argv[3]
subprocess.call([sys.argv[1], "assemble{0}".format(sys.argv[2])], cwd=app_path)