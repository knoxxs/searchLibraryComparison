#!/usr/bin/env python

'''
Basic pylucene indexing / search example.
'''
import sys, lucene, unittest
import os, shutil, time
import traceback
import TrecDocIterator

from java.io import File, StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import RAMDirectory, FSDirectory
from org.apache.lucene.util import Version

def indexDocs(writer, fileX):
  # do not try to index files that cannot be read
  if fileX.canRead():
    if fileX.isDirectory():
      files = fileX.list();
      # an IO error could occur
      if files != None:
        for i in range(len(files)):
          indexDocs(writer, File(fileX, files[i]))
    else:
      docs = TrecDocIterator.TrecDocIterator(fileX)
      while docs.hasNext():
        doc = docs.next();
        if doc != None and doc.getField("contents") != None:
          writer.addDocument(doc);

def main():
  lucene.initVM()  #Start up the Java Virtual Machine
  docPath = "data/"
  indexPath = "index/"
  create = True
  docDir = File(docPath)
  if not docDir.exists() or not docDir.canRead():
    print "Document directory '" +docDir.getAbsolutePath()+ "' does not exist or is not readable, please check the path"
    sys.exit(1)

  startTime = time.time()
  try:
    print "Indexing to directory '" + indexPath + "'..."

    direc = FSDirectory.open(File(indexPath))
    analyzer = StandardAnalyzer(Version.LUCENE_41)
    iwc = IndexWriterConfig(Version.LUCENE_41, analyzer)

    if (create):
      # Create a new index in the directory, removing any previously indexed documents:
      iwc.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    else:
      # Add new documents to an existing index:
      iwc.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND)
    
    # Optional: for better indexing performance, if you
    # are indexing many documents, increase the RAM
    # buffer.  But if you do this, increase the max heap
    # size to the JVM (eg add -Xmx512m or -Xmx1g):
    
    iwc.setRAMBufferSizeMB(256.0)

    writer = IndexWriter(direc, iwc)
    indexDocs(writer, docDir)

    # NOTE: if you want to maximize search performance,
    # you can optionally call forceMerge here.  This can be
    # a terribly costly operation, so generally it's only
    # worth it when your index is relatively static (ie
    # you're done adding documents to it):
    
    # writer.forceMerge(1)

    writer.close()

    endTime = time.time()
    print str(endTime- startTime) + " total milliseconds"

  except Exception, e:
    print "Ohh"
    print e
    print traceback.format_exc()

main()