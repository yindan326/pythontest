import re
import os

def scanFolder(path):
	files = os.listdir(path)
	for file_name in files:
		full_name = os.path.join(path,file_name)
		if not os.path.isdir(full_name) and full_name.find('.lua') != -1:
			replaceFile(full_name)

def replaceFile(file_name):
	print files_name
	current_file = open(file_name, 'r+')
	lines = current_file.readlines()

	needreplace = True
	flag = False
	src = ''
	des = ''
	for i in range(0,len(lines)):
		line = lines[i]
		if re.match('--',line) != None:#注释的地方不处理
			continue

		if line.find("result['Layer']=cc.Node:create()") != -1:#已经换过就不用换了
			needreplace = False
			break

		if line.find('local reslut={}') != -1:
			flag = True

		if line.find('addChild') != -1:
			tmpsrc = line[0:line.find(':')].strip()
			tmpdes = "reslut['" + tmpsrc + "']"
			line = line.replace(tmpsrc, tmpdes, 1)
			lines[i] = line

		if line.find("reslut['root']") != -1:
			tmpsrc = line[line.find('=')+1:].strip()
			tmpdes = "reslut['" + tmpsrc + "']"
			line = line.replace(tmpsrc, tmpdes, 1)
			lines[i] = line

		if flag == True:
			if re.match('local', line) != None and (line.find('create') != -1 or line.find('Create') != -1) and line.find('=') != -1:
				src = line[5:line.find('=')].strip()
				des = "reslut['" + src + "']"
				line = line.replace(src, des, 1)
				lines[i] = line[6:]
			else
				if src != '' and des != '':
					if src in line:
						line = line.replace(src, des, 1)
						lines[i] = line

	if needreplace == True:#不加也可以
		current_file.seek(0)
		current_file.truncate()
		current_file.writelines(lines)
		current_file.close()

replaceFile("./UIOperationIcon.lua")