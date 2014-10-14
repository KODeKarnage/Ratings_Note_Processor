
try:
	from xml.etree.cElementTree import XML
except ImportError:
	from xml.etree.ElementTree import XML
import zipfile


# https://gist.github.com/etienned/7539105 
"""
Module that extract text from MS XML Word document (.docx).
(Inspired by python-docx <https://github.com/mikemaccana/python-docx>)
"""
 
WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
SECT = WORD_NAMESPACE + 'p'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
 
 
def get_docx_text(path):
	"""
	Take the path of a docx file as argument, return the text in unicode
	in the form of a list.
	"""
	document = zipfile.ZipFile(path)
	xml_content = document.read('word/document.xml')
	document.close()
	tree = XML(xml_content)
 
	paragraphs = []
	for paragraph in tree.getiterator(PARA):
		texts = [node.text.encode('utf-8')
				 for node in paragraph.getiterator(TEXT)
				 if node.text]
		if texts:
			paragraphs.append(''.join(texts))
 
	return paragraphs



 
# def get_docx_text(path):
# 	"""
# 	Take the path of a docx file as argument, return the text in unicode
# 	in the form of a list.
# 	"""
# 	document = zipfile.ZipFile(path)
# 	xml_content = document.read('word/document.xml')
# 	document.close()
# 	tree = XML(xml_content)
 
# 	sections = []
# 	for section in tree.getiterator(SECT):

# 		paragraphs = []
# 		for paragraph in section.getiterator(PARA):
# 			print 'para'
# 			texts = [node.text.encode('utf-8')
# 					 for node in paragraph.getiterator(TEXT)
# 					 if node.text]
# 			if texts:
# 				paragraphs.append(''.join(texts))

# 		print str(paragraphs)

# 		if paragraphs:
# 			sections.append(''.join(paragraphs))

 
# 	return sections    