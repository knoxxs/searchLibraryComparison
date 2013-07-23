#!/usr/bin/env python

import sys, lucene, unittest
import os, shutil, time
import traceback

from java.io import File

from org.apache.lucene.analysis import Analyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document
from org.apache.lucene.index import DirectoryReader, IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, Query, ScoreDoc, TopDocs
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.util import Version

""" Simple command-line based search demo. """
class SearchFiles:

  def __init__(self):
    pass

  """ Simple command-line based search demo. """
  def main(self, index="index", field="contents", repeat=0, queries=None, queryString=None, raw=False, hitsPerPage=10):
    lucene.initVM()  #Start up the Java Virtual Machine
    reader = DirectoryReader.open(FSDirectory.open(File(index)))
    searcher = IndexSearcher(reader)
    analyzer = StandardAnalyzer(Version.LUCENE_41)

    inn = None
    if queries != None:
      inn = open(queries, "r")
    else:
      pass
      inn = sys.stdin
    parser = QueryParser(Version.LUCENE_41, field, analyzer)
    while True:
      if queries == None and queryString == None:
        print("Enter query: ")

      line = queryString if queryString != None else inn.readline()

      if line == None or len(line) == -1:
        break

      line = line.strip()
      if len(line) == 0:
        break
      
      query = parser.parse(line)
      print "Searching for: " + query.toString(field)
            
      if (repeat > 0):
        start = Date()
        for i in range(repeat):
          searcher.search(query, None, 100)
        end = Date()
        print "Time: "+(end.getTime()-start.getTime())+"ms"

      self.doPagingSearch(inn, searcher, query, hitsPerPage, raw, queries == None and queryString == None)

      if (queryString != None):
        break
    reader.close()

    # This demonstrates a typical paging search scenario, where the search engine presents 
    # pages of size n to the user. The user can then go to the next page if interested in
    # the next hits.

    # When the query is executed for the first time, then only enough results are collected
    # to fill 5 result pages. If the user wants to page beyond this limit, then the query
    # is executed another time and all hits are collected.
   
   
  def doPagingSearch(self, inn, searcher, query, hitsPerPage, raw, interactive):
    # Collect enough docs to show 5 pages
    results = searcher.search(query, 5 * hitsPerPage)
    hits = results.scoreDocs
    
    numTotalHits = results.totalHits
    print (str(numTotalHits) + " total matching documents")

    start = 0
    end = min(numTotalHits, hitsPerPage)
        
    while True:
      if end > len(hits):
        print ("Only results 1 - " + hits.length +" of " + numTotalHits + " total matching documents collected.")
        print ("Collect more (y/n) ?")
        line = inn.readline()
        if (line.length() == 0 or line.charAt(0) == 'n'):
          break

        hits = searcher.search(query, numTotalHits).scoreDocs
      
      end = min(len(hits), start + hitsPerPage)
      
      for i in range(start, end):
        if (raw):
          print ("doc="+hits[i].doc+" score="+hits[i].score)
          continue

        doc = searcher.doc(hits[i].doc)
        path = doc.get("docno")
        if (path != None):
          print ((i+1) + ". " + path)
          title = doc.get("title")
          if (title != None):
            print ("   Title: " + doc.get("title"))
        else:
          print ((i+1) + ". " + "No path for this document")

      if (not interactive or end == 0):
        break

      if (numTotalHits >= end):
        quit = false
        while (True):
          print("Press ")
          if (start - hitsPerPage >= 0):
            print("(p)revious page, ")  
          if (start + hitsPerPage < numTotalHits):
            print("(n)ext page, ")
          print ("(q)uit or enter number to jump to a page.")
          
          line = inn.readline()
          if (line.length() == 0 or line.charAt(0)=='q'):
            quit = true
            break
          if (line.charAt(0) == 'p'):
            start = Math.max(0, start - hitsPerPage)
            break
          elif(line.charAt(0) == 'n'):
            if (start + hitsPerPage < numTotalHits):
              start+=hitsPerPage
            break
          else:
            page = Integer.parseInt(line)
            if ((page - 1) * hitsPerPage < numTotalHits):
              start = (page - 1) * hitsPerPage
              break
            else:
              print ("No such page")
        if (quit): break
        end = Math.min(numTotalHits, start + hitsPerPage)

sr = SearchFiles()
sr.main()