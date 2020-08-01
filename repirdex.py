import getopt,sys,re,base64

def parse_inst(name):
	"""
	parse & format .bin
	"""
	code = list()
	with open(name,"r") as f:
		data = f.read()
	insts = data.split(';')
	for inst in insts:
		offset = re.search(r'offset:(\d*),',inst)
		if not offset:
			continue
		#print offset.group(1)
		name = re.search(r'name:([^)]*\)),',inst)
		if not name:
			continue
		#print len.group(1)
		ins = re.search(r'ins:(\S*)}',inst)
		if not ins:
			continue
		#print ins.group(1)
		len = re.search(r'len:(\d*),',inst)
		if not len:
			continue
		#print len.group(1)
		code.append({"offset":offset.group(1),"name":name.group(1),"ins":ins.group(1),"len":len.group(1)})
	return code
	
def repir_dex(name,code):
	"""
	repir dex
	"""
	dex_file = open(name,"r+b")
	for inst in code:
		if dex_file.seek(int(inst["offset"])) == -1:
			continue
		inst_bytes = base64.b64decode(inst["ins"])
		dex_file.write(inst_bytes)
		print inst["name"]," repired"
		#print inst["name"]," offset:",inst["offset"],"len:",inst["len"],":".join("{:02x}".format(ord(c)) for c in inst_bytes)
	dex_file.close()

def init():
	global filename
	global insfilename
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:d:i:", ["dumpdexfile=", "insfile="])
	except getopt.GetoptError:
		print 'Fart.py -d <dumpdexfile> -i <insfile>'
		sys.exit(2)
	if len(opts)<=0:
		print 'Fart.py -d <dumpdexfile> -i <insfile>'
		sys.exit()
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print 'Fart.py -d <dumpdexfile> -i <insfile>'
			sys.exit()
		if opt in ("-d", "--dumpdexfile"):
			filename = arg
		elif opt in ("-i", "--insfile"):
			insfilename = arg
	print 'dumpdex file:', filename
	print 'ins file:', insfilename

def main():
	code = parse_inst(insfilename)
	dex = repir_dex(filename,code)
	
if __name__ == "__main__":
	init()
	main()