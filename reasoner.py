from rdflib import Graph
from rdflib import RDF,RDFS

def readFile(inputFilePath):
	g=Graph()
	g.parse(inputFilePath)
	return g


def reasoner1(graph):
	# takes care of 
	i=0
	
	rangeDictionary={}
	for subject,predicate,obj in graph:
		if(str(predicate)=="http://www.w3.org/2000/01/rdf-schema#range"):
			rangeDictionary[str(subject)]=str(obj)
	for subject,predicate,obj in graph:
		if str(predicate) in rangeDictionary:
			print(str(obj),RDF.type,rangeDictionary[str(predicate)])

	domainDictionary={}
	for subject,predicate,obj in graph:
		if str(predicate)=='http://www.w3.org/2000/01/rdf-schema#domain':
			domainDictionary[str(subject)]=str(obj)
	for subject,predicate,obj in graph:
		if str(predicate) in domainDictionary:
			print("hey oh")
			print(str(subject),RDF.type,domainDictionary[str(predicate)])

			


reasoner1(readFile("sampleinput.ttl"))

