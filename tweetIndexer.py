#!/usr/bin/env python

'''
Basic pylucene indexing / search example.
'''
import sys, lucene, unittest
import os, shutil

from java.io import File, StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import RAMDirectory
from org.apache.lucene.util import Version

def main(argv=None):
    lucene.initVM()  #Start up the Java Virtual Machine
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    # Store the index in memory:
    directory = RAMDirectory()
    # To store an index on disk, use this instead:
    #Directory directory = FSDirectory.open("/tmp/testindex")
    config =  IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
    iwriter = IndexWriter(directory, config)
    text = "This is the text to be indexed."
    filePath = "data/twitter/tweets.json"
    print df
    f = open(filePath, 'r')
    for line in f:
        doc = Document()
        doc.add(Field("text", line, TextField.TYPE_STORED))
        iwriter.addDocument(doc)
    iwriter.close()
    print directory.sizeInBytes()
    print 1
    # Now search the index:
    ireader = DirectoryReader.open(directory)
    isearcher = IndexSearcher(ireader)
    # Parse a simple query that searches for "text":
    parser = QueryParser(Version.LUCENE_CURRENT, "text", analyzer)
    query = parser.parse("hello")
    hits = isearcher.search(query, None, 1)
    print hits.totalHits
    hits = hits.scoreDocs
    # Iterate through the results:
    for hit in hits:
      hitDoc = isearcher.doc(hit.doc)
      print hitDoc.get("text")
    ireader.close()
    directory.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))