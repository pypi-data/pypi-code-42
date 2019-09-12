# -*- coding: utf-8 -*-
#cython: language_level=2
from __future__ import unicode_literals
from __future__ import division

import os
import errno
import importlib

from songfinder import globalvar

try:
	fileName = os.path.splitext( os.path.split(__file__)[1] )[0]
	module = importlib.import_module('lib.%s_%s'%(fileName, globalvar.arch))
	print("Using compiled version %s module"%fileName)
	globals().update(
		{n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__')
		else
		{k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
	})
except (ImportError, NameError):
	# print(traceback.format_exc())

	import datetime
	import unicodedata
	try:
		import cython
	except ImportError:
		pass

	def safeUnicode(text):
		try:
			text = unicode(text, 'utf-8')
		except (TypeError, NameError): # unicode is a default on python 3
			pass
		return text

	def enleve_accents(text):
		"""
		Strip accents from input String.

		:param text: The input string.
		:type text: String.

		:returns: The processed String.
		:rtype: String.
		"""
		text = safeUnicode(text)
		text = unicodedata.normalize('NFD', text)
		text = text.encode('ascii', 'ignore')
		text = text.decode("utf-8")
		return str(text)

	def enleve_accents_unicode(text):
		"""
		Strip accents from input String.

		:param text: The input string.
		:type text: String.

		:returns: The processed String.
		:rtype: String.
		"""
		text = unicodedata.normalize('NFD', text)
		text = text.encode('ascii', 'ignore')
		text = text.decode("utf-8")
		return str(text)

	def get_file_name(full_path):
		file_name = os.path.splitext( os.path.split(full_path)[1] )[0]
		return file_name

	def get_file_name_ext(full_path):
		file_name_ext = os.path.split(full_path)[1]
		return file_name_ext

	def get_path(full_path):
		path = os.path.split(full_path)[0]
		return path

	def get_ext(full_path):
		ext = os.path.splitext(full_path)[1]
		return ext

	def get_file_path(full_path):
		ext = os.path.splitext(full_path)[0]
		return ext

	def upper_first(mot):
		if len(mot) > 1:
			mot = mot[0].upper() + mot[1:]
		else:
			mot = mot.upper()
		return mot

	def cree_nom_sortie(chemin_sets):
		proch_dimanche = datetime.timedelta(days = 6-datetime.datetime.today().weekday())
		nom_sortie = str(datetime.date.today()+ proch_dimanche)
		return noOverrite(nom_sortie)

	def noOverrite(inName):
		while os.path.isfile(inName):
			ext = get_ext(inName)
			name = get_file_name(inName)
			underScore = name.rfind('_')
			if underScore != -1 and name[underScore+1:].isdigit():
				num = int(name[underScore+1:])
				inName = inName.replace('_%d%s'%(num, ext), '_%d%s'%(num+1, ext))
			else:
				inName = inName.replace('%s'%ext, '_1%s'%ext)
		return inName

	def strip_perso(text, car):
		while text[-len(car):] == car:
			text = text[:-len(car)]
		while text[:len(car)] == car:
			text = text[len(car):]
		return text

	def splitPerso(listText, listSep, listStype, i):
		try:
			l = cython.declare(cython.int)
			j = cython.declare(cython.int)
			k = cython.declare(cython.int)
		except NameError:
			pass
		tmp = []
		l=0
		for j,text in enumerate(listText):
			newListText = text.split(listSep[i])
			for k,elem in enumerate(newListText):
				tmp.append(strip_perso(elem, '\n'))
				if k > 0:
					listStype.insert(l-1, listSep[i])
				l = l+1
		if i+1 < len(listSep):
			tmp, listStype = splitPerso(tmp, listSep, listStype, i+1)
		return tmp, listStype

	def supressB(text, deb, fin):
		try:
			i = cython.declare(cython.int)
		except NameError:
			pass
		subList = [sub.split(fin,1)[1] if i>0 and len(sub.split(fin,1))>1 \
									else sub \
									for (i,sub) in enumerate(text.split(deb))]
		newText = ''.join(subList)
		return newText

	def getB(text, deb, fin):
		try:
			i = cython.declare(cython.int)
		except NameError:
			pass
		outListe = [sub.split(fin,1)[0] for (i,sub) in enumerate(text.split(deb)) if i>0]
		return outListe

	def matchPara(text1, text2):
		try:
			lengh = cython.declare(cython.int)
			matches = cython.declare(cython.int)
			diff = cython.declare(cython.int)
			out = cython.declare(cython.float)
		except NameError:
			pass
		text1 = '%s\n'%text1
		text2 = '%s\n'%text2
		text1 = supressB(text1, '\\ac', '\n')
		text2 = supressB(text2, '\\ac', '\n')
		text1 = text1.strip('\n')
		text2 = text2.strip('\n')
		listMot1 = text1.split(' ')
		listMot2 = text2.split(' ')
		lengh = max(len(listMot1), len(listMot2))
		matches = len(set(listMot1) & set(listMot2))
		diff = len(set(listMot1) ^ set(listMot2))
		if diff == 0:
			out = 10000.
		else:
			out = matches/diff
		return out

	def takeOne(stypeProcess, listIn):
		# Take the first slide of selected type
		ok = True
		newList = []
		for elem in listIn:
			if elem[0] == stypeProcess:
				if ok:
					ok = False
					newList.append(elem)
			else:
				newList.append(elem)

		return newList

	def cleanFile(fileRm):
		try:
			os.remove(fileRm)
		except (OSError, IOError) as error:
			if error.errno == errno.ENOENT:
				pass
			else:
				raise

	def indent(elem, level=0):
		i = "\r\n" + level*"  "
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "  "
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
			for elem in elem:
				indent(elem, level+1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i

	def noNewLine(text, command, newline):
		try:
			deb = cython.declare(cython.int)
			fin = cython.declare(cython.int)
		except NameError:
			pass
		deb = 0
		fin = 0
		end = '}'
		for _ in range(10000):
			deb = text.find(command, fin)+len(command)
			fin = text.find(end, deb)+len(end)
			if deb == -1 or fin == -1:
				break
			elif text[fin:fin+len(newline)] == newline:
				text = text[:fin] + text[fin+len(newline):]
		return text

	def isNumber(s):
		try:
			float(s)
			return True
		except ValueError:
			return False
