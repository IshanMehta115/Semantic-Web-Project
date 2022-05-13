from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF , XSD
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF, XSD, RDFS
from rdflib import Namespace


from rdflib import Graph
from rdflib import RDF,RDFS



#subclass transitivity

visited = []        
def printAndExplore(subject, lst, map):
        relation = '<http://www.w3.org/2000/01/rdf-schema#subClassOf>'
        for obj in lst:
            if ((obj in visited) == False):      # visited.contains(obj) == false
                visited.append(obj)
                print('<' + subject + '> ' + relation + ' <' + obj + ">.")
                #print(obj in map.keys())
                if ((obj in map.keys()) == True) :
                    #print("ENTERED IN IF BLOCK")
                    printAndExplore(subject, map[obj], map)
                #visited.append(obj)
            
    
def predicateContainSubClass(s) :
    if ('/' in s) :                                                              #s.contains('/')
        ind = s.rindex('/')
        substring = s[ind + 1:]
        if (substring == 'rdf-schema#subClassOf') :
            return True
        else:
            return False
    else:
        return False

    
def subclassTransitivityEntailment(g):
    map = {}
    for s, p, o in g:
        s = str(s)
        p = str(p)
        o = str(o)
        #print(s)
        #print(p)
        #print(o)
        if (predicateContainSubClass(p)) :
            if ((s in map.keys()) == False) :
                map[s] = []
            lst = map[s]
            lst.append(o)

    relation = '<http://www.w3.org/2000/01/rdf-schema#subClassOf>'

    for subject, lst in map.items():
        visited.clear()
        #print(visited)
        #print(subject + "**" + str(lst))
        printAndExplore(subject, lst, map)

        
        
        
        
        
#subproperty transitivity

visited = []        
def printAndExplore2(subject, lst, map):
        relation = '<http://www.w3.org/2000/01/rdf-schema#subPropertyOf>'
        for obj in lst:
            if ((obj in visited) == False):      # visited.contains(obj) == false
                visited.append(obj)
                print('<' + subject + '> ' + relation + ' <' + obj + ">.")
                #print(obj in map.keys())
                if ((obj in map.keys()) == True) :
                    #print("ENTERED IN IF BLOCK")
                    printAndExplore2(subject, map[obj], map)
                #visited.append(obj)
            
    
def predicateContainSubProperty(s) :
    if ('/' in s) :                                                              #s.contains('/')
        ind = s.rindex('/')
        substring = s[ind + 1:]
        if (substring == 'rdf-schema#subPropertyOf') :
            return True
        else:
            return False
    else:
        return False


def subpropertyTransitivityEntailment(g):
    map = {}    

    for s, p, o in g:
        s = str(s)
        p = str(p)
        o = str(o)
        #print(s)
        #print(p)
        #print(o)
        if (predicateContainSubProperty(p)) :
            if ((s in map.keys()) == False) :
                map[s] = []
            lst = map[s]
            lst.append(o)

    relation = '<http://www.w3.org/2000/01/rdf-schema#subPropertyOf>'

    #print(map)
    for subject, lst in map.items():
        visited.clear()
        #print(visited)
        #print(subject + "**" + str(lst))    
        printAndExplore2(subject, lst, map)    
        
        
def subclassTransitivityIllustration():
    n = Namespace("http://iiitd.ac.in/course/sweb/project/")
    g = Graph()
    human = n.human
    trainer = n.trainer
    teacher = n.teacher
    principal = n.principal

    g.add((principal, RDFS.subClassOf, teacher))
    g.add((teacher, RDFS.subClassOf, trainer))
    g.add((trainer, RDFS.subClassOf, human))
    subclassTransitivityEntailment(g)


def subpropertyTransitivityIllustration():
    n = Namespace("http://iiitd.ac.in/course/sweb/project/")
    g = Graph()
    financeManagerOf = n.financeManagerOf
    managerOf = n.managerOf
    employeeOf = n.employeeOf
    humanOf = n.humanOf

    g.add((financeManagerOf, RDFS.subPropertyOf, managerOf))
    g.add((managerOf, RDFS.subPropertyOf, employeeOf))
    g.add((employeeOf, RDFS.subPropertyOf, humanOf))
    subpropertyTransitivityEntailment(g)
    



#ILLUSTRATION
   
subclassTransitivityIllustration()
print()
subpropertyTransitivityIllustration()







def readFile(inputFilePath):
    g=Graph()
    g.parse(inputFilePath)
    return g


def reasoner1(graph):
    # takes care of 
    i=0
    # for subject,predicate,obj in graph:
    # 	print(str(predicate))
    # return;
    rangeDictionary={}
    # range property
    for subject,predicate,obj in graph:
        if(str(predicate)=="http://www.w3.org/2000/01/rdf-schema#range"):
            rangeDictionary[str(subject)]=str(obj)
    for subject,predicate,obj in graph:
        if str(predicate) in rangeDictionary:
            print(str(obj),RDF.type,rangeDictionary[str(predicate)])

    domainDictionary={}
    # domain property
    for subject,predicate,obj in graph:
        if str(predicate)=='http://www.w3.org/2000/01/rdf-schema#domain':
            domainDictionary[str(subject)]=str(obj)
    for subject,predicate,obj in graph:
        if str(predicate) in domainDictionary:
            print("hey oh")
            print(str(subject),RDF.type,domainDictionary[str(predicate)])
    # every subject,object is a resource property
    for subject,predicate,obj in graph:
        print(str(subject),RDF.type,RDFS.Resource)
        print(str(obj),RDF.type,RDFS.Resource)
    # every class is its own subclass

    for subject,predicate,obj in graph:
        if(str(obj)=="http://www.w3.org/2000/01/rdf-schema#Class"):
            print(str(subject),RDFS.subClassOf,str(subject))


#reasoner1(readFile("sampleinput.ttl"))



