import subprocess

cmdline = ["talys", "talys.inp", "talys.out"]
working_directory = r"C:\Users\dimitristsatsis\Desktop\talys\talys\samples"

output = subprocess.run(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory, text=True)
