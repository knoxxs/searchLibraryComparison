#!/usr/bin/env python

import cStringIO 
import re

from org.apache.lucene.document import Document, Field, StringField, TextField

class TrecDocIterator:
  fl = None
  at_eof = False

  def __init__(self, fileObj):
    global at_eof,fl
    fl = open(fileObj.toString(), 'r')
    print "Reading " + fileObj.toString()
    at_eof = False


  def hasNext(self):
    return (not at_eof)

  def next(self):
    global at_eof
    doc = Document()
    try:
      buf = cStringIO.StringIO()
      docno_tag = re.compile("<DOCNO>\\s*(\\S+)\\s*<")
      in_doc = False
      while (True):
        line = fl.readline()
        if (line == ""):
          at_eof = True
          break
        if not in_doc:
					if line.startswith("<DOC>"):
						in_doc = true
					else:
						continue
        if line.startswith("</DOC>"):
					in_doc = false
					buf.write(line)
					break

        mtch = docno_tag.match(line)
        if mtch:
					docno = mtch.group(1)
					doc.add(StringField("docno", docno, Field.Store.YES))
        buf.write(line)

      value = buf.getvalue()
      if len(value) > 0:
				doc.add(TextField("contents", value, Field.Store.NO))	
    except IOError:
			print IOError
    
    return doc

  def remove(self):
		# Do nothing, but don't complain
    pass