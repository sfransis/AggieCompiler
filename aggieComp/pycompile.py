import os, sys, subprocess, tempfile, time


# Creating a temporary folder and returning the temporary folder path
TempFile = tempfile.mkdtemp(suffix='_test', prefix='python_')
# Filename
FileNum = int(time.time() * 1000)
# python compiler location
EXEC = sys.executable



# get python version
def get_version():
    v = sys.version_info
    version = "python %s.%s" % (v.major, v.minor)
    return version


# Getting the py file name
def get_pyname():
    global FileNum
    return 'test_%d' % FileNum


# Receive code to write to file 
def write_file(pyname, code):
    fpath = os.path.join(TempFile, '%s.py' % pyname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(code)
    print('file path: %s' % fpath)
    return fpath


# Encoding
def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')



def main(code):
    r = dict()
    r["version"] = get_version()
    pyname = get_pyname()
    fpath = write_file(pyname, code)
    try:
		# subprocess.check_output is the parent process waits for the child process to complete,
  		# and returns the output result of the child process to the standard output
        # stderr is the type of standard output
        # subprocess.check_output Execute a shell command
        outdata = decode(subprocess.check_output([EXEC, fpath], stderr=subprocess.STDOUT, timeout=10))
    except subprocess.CalledProcessError as e:
        #Error case handling of output
        r["code"] = 'Error'
        r["output"] = decode(e.output)
        return r
    else:
        # Successfully returned data
        r['output'] = outdata
        r["code"] = "Success"
        return r
    finally:
        # deleting the file and it automatically deleted without deleting the temporary file 
        try:
            os.remove(fpath)
        except Exception as e:
            exit(1)

if __name__ == '__main__':
    code = "print(11);print(12)"
    print(main(code))