import subprocess

# Run the first Python file
process1 = subprocess.Popen(['python', 'keyhandler.py'])

# Run the second Python file
process2 = subprocess.Popen(['python', 'localhost.py'])

# Wait for both processes to complete
process1.wait()
process2.wait()