import sys
import traceback

from .grammar       import parse, TreeNode
from .commands.base import Proc

def filter_ascii(string):
	string = ''.join(char for char in string if ord(char) < 128 and ord(char) > 32 or char in " ")
	return string

###

ELF_BIN_ARM  = "\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00(\x00\x01\x00\x00\x00h\xc2\x00\x004\x00\x00\x00X^\x01\x00\x02\x00\x00\x054\x00 \x00\x08\x00(\x00\x1c\x00\x1b\x00\x01\x00\x00p\xc0X\x01\x00\xc0\xd8\x01\x00\xc0\xd8\x01\x00\x18\x00\x00\x00\x18\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x06\x00\x00\x004\x00\x00\x004\x80\x00\x004\x80\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x05\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x004\x01\x00\x004\x81\x00\x004\x81\x00\x00\x13\x00\x00\x00\x13\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\xdcX\x01\x00\xdcX\x01\x00\x05\x00\x00\x00\x00\x80\x00\x00\x01\x00\x00\x00\xdcX\x01\x00\xdcX\x02\x00\xdcX\x02\x00\x1c\x04\x00\x00\xbc\x10\x00\x00\x06\x00\x00\x00\x00\x80\x00\x00\x02\x00\x00\x00\xe8X\x01\x00\xe8X\x02\x00\xe8X\x02\x00\x08\x01\x00\x00\x08\x01\x00\x00\x06\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00H\x01\x00\x00H\x81\x00\x00H\x81\x00\x00D\x00\x00\x00D\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00Q\xe5td\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x04\x00\x00\x00/lib/ld-linux.so.3\x00\x00\x04\x00\x00\x00\x10\x00\x00\x00\x01\x00\x00\x00GNU\x00\x00\x00\x00\x00\x02\x00\x00\x00\x06\x00\x00\x00\x1b\x00\x00\x00\x04\x00\x00\x00\x14\x00\x00\x00\x03\x00\x00\x00GNU\x00\x02Tz0\x80\x94\xc2\x8e%\xf1\xa4\xad\xc7D\xa9\x91q\x94\xdb\na\x00\x00\x00\x06\x00\x00\x00 \x00\x00\x00\n\x00\x00\x00\x00I\x10\x92\x02D\x1b&@\x10@\xe0B\x00`\x00\x91AA\x10\x00r\x11\x11aH\x14(\x00\x00\x00\x00\x08\x00\x00\x80\x90\t\x00 \x08\x00*\x00@\x00$\xad\x11\x10\x81,(\x00\x00\t@J!\x91\x19\xadA\x04\x80IE\x85\x85\xf0\x88\xb3h\x80\x02H\x08\x80\x80\x00\x08\x01(d\x0e!M\xe0\xa8D\x94\x02 \x00\x08\x01\x87)\x00\x08\n\x00J\x08\x0e\x01\xc0-\x00 @\x18\x80d\xe6 \x81\x02\x00\x89\n\x90\x00$\x0e\x8c\xb0(\x06\x00\x00\x00\x08\x00\x00\x00\t\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00\x00\x12\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00\x19\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1d\x00\x00\x00\x1e\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00!\x00\x00\x00%\x00\x00\x00\x00\x00\x00\x00'\x00\x00\x00)\x00\x00\x00\x00\x00\x00\x00*\x00\x00\x00,\x00\x00\x000\x00\x00\x002\x00\x00\x00\x00\x00\x00\x003\x00\x00\x00\x00\x00\x00\x006\x00\x00\x008\x00\x00\x00:\x00\x00\x00<\x00\x00\x00>\x00\x00\x00?\x00\x00\x00A\x00\x00\x00G\x00\x00\x00I\x00\x00\x00\x00\x00\x00\x00J\x00\x00\x00\x00\x00\x00\x00K\x00\x00\x00L\x00\x00\x00\x00\x00\x00\x00N\x00\x00\x00R\x00\x00\x00S\x00\x00\x00T\x00\x00\x00U\x00\x00\x00\x00\x00\x00\x00V\x00\x00\x00W\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00X\x00\x00\x00Y\x00\x00\x00Z\x00\x00\x00\\\x00\x00\x00^\x00\x00\x00`\x00\x00\x00c\x00\x00\x00d\x00\x00\x00f\x00\x00\x00h\x00\x00\x00i\x00\x00\x00k\x00\x00\x00n\x00\x00\x00q\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00t\x00\x00\x00\x00\x00\x00\x00u\x00\x00\x00v\x00\x00\x00y\x00\x00\x00z\x00\x00\x00\x00\x00\x00\x00{\x00\x00\x00\x00\x00\x00\x00}\x00\x00\x00~\x00\x00\x00\x7f\x00\x00\x00\x80\x00\x00\x00\x81\x00\x00\x00\x82\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\x08,\xae\xff_\x96\x93\x1c\x03}\x1eL\xa3Z\xef\x90V\xdb\x93\x1c\xa8vbICw)\x91,2@\xfd\xda\x80A\xb7\xed\xe9C+\xf1\x81B\x84\xcf\x18L\x0fvT<\x94\xca\x96\x93\x1c\xcd?\x0c\xaf\x88j\x06\xaf\x8dm\x94\x06\x08~\x92\x1c!t\xb0\x02\xe2\xad\xc6\x1b.N=\xf6\xdb\xf7\x00^\x01\xaf4\xe8_t;\xc5"

ELF_BIN_X86  = "\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00>\x00\x01\x00\x00\x00P\x1c\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\xb8\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x008\x00\t\x00@\x00\x1c\x00\x1b\x00\x06\x00\x00\x00\x05\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\xf8\x01\x00\x00\x00\x00\x00\x00\xf8\x01\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x008\x02\x00\x00\x00\x00\x00\x008\x02\x00\x00\x00\x00\x00\x008\x02\x00\x00\x00\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98m\x00\x00\x00\x00\x00\x00\x98m\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x01\x00\x00\x00\x06\x00\x00\x00\xf0{\x00\x00\x00\x00\x00\x00\xf0{ \x00\x00\x00\x00\x00\xf0{ \x00\x00\x00\x00\x00\x90\x04\x00\x00\x00\x00\x00\x000\x06\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x02\x00\x00\x00\x06\x00\x00\x00X|\x00\x00\x00\x00\x00\x00X| \x00\x00\x00\x00\x00X| \x00\x00\x00\x00\x00\xf0\x01\x00\x00\x00\x00\x00\x00\xf0\x01\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00T\x02\x00\x00\x00\x00\x00\x00T\x02\x00\x00\x00\x00\x00\x00T\x02\x00\x00\x00\x00\x00\x00D\x00\x00\x00\x00\x00\x00\x00D\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00P\xe5td\x04\x00\x00\x00d`\x00\x00\x00\x00\x00\x00d`\x00\x00\x00\x00\x00\x00d`\x00\x00\x00\x00\x00\x00D\x02\x00\x00\x00\x00\x00\x00D\x02\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00Q\xe5td\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00R\xe5td\x04\x00\x00\x00\xf0{\x00\x00\x00\x00\x00\x00\xf0{ \x00\x00\x00\x00\x00\xf0{ \x00\x00\x00\x00\x00\x10\x04\x00\x00\x00\x00\x00\x00\x10\x04\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00/lib64/ld-linux-x86-64.so.2\x00\x04\x00\x00\x00\x10\x00\x00\x00\x01\x00\x00\x00GNU\x00\x00\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x14\x00\x00\x00\x03\x00\x00\x00GNU\x00Y\xde\xf0\x1bLK<H}\x8b\xb8\x98mI\xbeo\xf4b8w\x03\x00\x00\x005\x00\x00\x00\x02\x00\x00\x00\x07\x00\x00\x00\x12\x01\xd2$\x12)\x00V`A\x00\x0e \x00\x00\x005\x00\x00\x009\x00\x00\x00@\x00\x00\x00\x04\x8b&\xa4(\x1d\x8c\x1c\x10\x8aM#\xc9MB#\xbcPv\x9e\xacK\xe3\xc0\x96\xa0\x89\x97F-\xe4\xde\xce,cr\xe4bA\xf59\xf2\x8b\x1c*\xd4\xb8\xd3\x1c\xedc*?\x04K\x86\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\x01\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<\x01\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf2\x01\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00s\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xca\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x001\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd9\x02\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00y\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x01\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

globalfiles = {
    "/proc/mounts": """/dev/root /rom squashfs ro,relatime 0 0
proc /proc proc rw,nosuid,nodev,noexec,noatime 0 0
sysfs /sys sysfs rw,nosuid,nodev,noexec,noatime 0 0
tmpfs /tmp tmpfs rw,nosuid,nodev,noatime 0 0
/dev/mtdblock10 /overlay jffs2 rw,noatime 0 0
overlayfs:/overlay / overlay rw,noatime,lowerdir=/,upperdir=/overlay/upper,workdir=/overlay/work 0 0
tmpfs /dev tmpfs rw,nosuid,relatime,size=512k,mode=755 0 0
devpts /dev/pts devpts rw,nosuid,noexec,relatime,mode=600 0 0
debugfs /sys/kernel/debug debugfs rw,noatime 0 0\n""",
    "/proc/cpuinfo": """processor       : 0
model name      : ARMv6-compatible processor rev 7 (v6l)
BogoMIPS        : 697.95
Features        : half thumb fastmult vfp edsp java tls 
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xb76
CPU revision    : 7

Hardware        : BCM2835
Revision        : 000e
Serial          : 0000000000000000\n""",
    "/bin/echo": ELF_BIN_ARM,
    "/bin/busybox": ELF_BIN_ARM
}

def instantwrite(msg):
	sys.stdout.write(msg)
	sys.stdout.flush()

class Env:
	def __init__(self, output=instantwrite):
		self.files   = {}
		self.deleted = []
		self.events  = {}
		self.output  = output

	def write(self, string):
		self.output(string)

	def deleteFile(self, path):
		if path in self.files:
		    self.deleted.append((path, self.files[path]))
		    del self.files[path]

	def writeFile(self, path, string):
		if path in self.files:
		    self.files[path] += string
		else:
		    self.files[path] = string

	def readFile(self, path):
		if path in self.files:
		    return self.files[path]
		elif path in globalfiles:
		    return globalfiles[path]
		else:
		    return None

	def listen(self, event, handler):
		self.events[event] = handler

	def action(self, event, data):
		if event in self.events:
		    self.events[event](data)
		else:
		    print(("WARNING: Event '" + event + "' not registered"))
		    
	def listfiles(self):
		return self.files

class RedirEnv:
	def __init__(self, baseenv, redir):
		self.baseenv = baseenv
		self.redir   = redir

	def write(self, string):
		self.baseenv.writeFile(self.redir, string)

	def deleteFile(self, path):
		self.baseenv.deleteFile(path)

	def writeFile(self, path, string):
		self.baseenv.writeFile(path, string)

	def readFile(self, path):
		return self.baseenv.readFile(path)

	def listen(self, event, handler):
		self.baseenv.listen(event, handler)

	def action(self, event, data):
		self.baseenv.action(event, data)
		    
	def listfiles(self):
		return self.baseenv.listfiles()

class Command:
    def __init__(self, args):
        self.args             = args
        self.redirect_from_f  = None
        self.redirect_to_f    = None
        self.redirect_append  = False
        self.shell            = Proc.get("exec")
        
    def redirect_to(self, filename):
        self.redirect_to_f = filename
        self.redirect_append = False
        
    def redirect_from(self, filename):
        self.redirect_from_f = filename
        
    def redirect_app(self, filename):
        self.redirect_to(filename)
        self.redirect_append = True

    def run(self, env):
        if self.isnone():
            return 0
        
        if self.redirect_to_f != None:
            if not(self.redirect_append):
                env.deleteFile(self.redirect_to_f)
            env = RedirEnv(env, self.redirect_to_f)
            
        return self.shell.run(env, self.args)
    
    def isnone(self):
        return len(self.args) == 0

    def __str__(self):
        return "cmd(" + " ".join(self.args) + ")"

class CommandList:

    def __init__(self, mode, cmd1, cmd2):
        self.mode = mode
        self.cmd1 = cmd1
        self.cmd2 = cmd2
        
    def redirect_to(self, filename):
        self.cmd1.redirect_to(filename)
        self.cmd2.redirect_to(filename)
        
    def redirect_from(self, filename):
        self.cmd1.redirect_from(filename)
        self.cmd2.redirect_from(filename)
        
    def redirect_app(self, filename):
        self.cmd1.redirect_app(filename)
        self.cmd2.redirect_app(filename)

    def run(self, env):
        ret = self.cmd1.run(env)
        if (self.mode == "&&"):
            if (ret == 0):
                return self.cmd2.run(env)
            else:
                return ret
        elif (self.mode == "||"):
            if (ret != 0):
                return self.cmd2.run(env)
            else:
                return ret
        elif (self.mode == ";"):
            if self.cmd2.isnone():
                return ret            
            return self.cmd2.run(env)
        else:
            print("WARN: Bad Mode")
            return 1
        
    def isnone(self):
        return self.cmd1.isnone() and self.cmd2.isnone()

    def __str__(self):
        return "(" + str(self.cmd1) + self.mode + str(self.cmd2) + ")"

class Actions(object):
    def make_arg_noquot(self, input, start, end, elements):
	    return input[start:end]

    def make_arg_quot(self, input, start, end, elements):
        return elements[1].text

    def make_list(self, input, start, end, elements):
        c1 = elements[0]
        
        if len(elements[1].elements) != 0:
            c2 = elements[1].elements[3]
            
            return CommandList(";", c1, c2)
        
        return c1
    
    def make_single(self, input, start, end, elements):
        c1 = elements[0]
        
        if len(elements[1].elements) != 0:
            c2 = elements[1].elements[3]
            op = elements[1].elements[1]
            
            return CommandList(op.text, c1, c2)
        
        return c1
    
    def make_pipe(self, input, start, end, elements):
        c1 = elements[0]
        
        if len(elements[1].elements) != 0:
            c2 = elements[1].elements[3]
            
            c1.redirect_to("/dev/pipe")
            c2.redirect_from("/dev/pipe")
            
            return CommandList(";", c1, c2)
        
        
        return c1
    
    def make_redir(self, input, start, end, elements):
        
        c = elements[0]
        
        for redirect in elements[1].elements:
            operator = redirect.elements[1].text
            filename = redirect.elements[3]
            
            if operator == ">":
                c.redirect_to(filename)
            elif operator == ">>":
                c.redirect_app(filename)
            elif operator == "<":
                c.redirect_from(filename)
            else:
                print("WARNING: unsupported redirect operator " + operator)
                
        return c
    
    def make_cmdbrac(self, input, start, end, elements):
        return elements[2]
    
    def make_args(self, input, start, end, elements):
        if isinstance(elements[0], str): 
            r = [ elements[0] ]
        else:
            r = []
        
        for arg in elements[1].elements:
            if isinstance(arg.elements[1], str):
                r.append(arg.elements[1])
        
        c = Command(r)
        
        return c

def run(string, env):
    c = parse(filter_ascii(string).strip(), actions=Actions())
    return c.run(env)

def test_shell():
    env = Env()
    while True:
        sys.stdout.write(" # ")
        sys.stdout.flush()
        line = sys.stdin.readline()
        if line == "":
            break
        if line == "\n":
            continue
        line = line[:-1] 
        tree = run(line, env)
        sys.stdout.flush()

