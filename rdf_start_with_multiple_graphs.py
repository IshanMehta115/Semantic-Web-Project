from argon2 import PasswordHasher
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF

'''
    Info about variables
    1) statements
    type    -   dict
    key     -   graph_name (string)
    value   -   statments (list)

    2) tripleId_to_triple
    type    -   dict
    key     -   graph_name (string)
    value   -   dict having key as triple id and value as triple strings

    3) tripleId_to_triple
    type    -   dict
    key     -   graph_name (string)
    value   -   dict having key as triple strings and value as triple id

    4) temp_statements
    type    -   list
    stores statements of triple being processed temporarily

'''
statements = {}
tripleId_to_triple = {}
triple_to_tripleId = {}
temp_statements  = []


def process_ntriple(triple_string, graph_name):
    global statements,triple_to_tripleId,tripleId_to_triple,temp_statements
    if graph_name not in statements:
        statements[graph_name] = []
    if graph_name not in tripleId_to_triple:
        tripleId_to_triple[graph_name] = {}
    if graph_name not in triple_to_tripleId:
        triple_to_tripleId[graph_name] = {}
    temp_statements = []
    process(triple_string, 1, graph_name)
    print("triple processed")
    print("following statements are added ->")
    for i in temp_statements:
        print(i + " .")
    statements[graph_name]+=temp_statements


def print_statements(graph_name):
    global statements
    if graph_name not in statements:
        print("graph with name " +graph_name + " not found")
        return
    print("\nstatements in " + graph_name + " are ->\n")
    for i in statements[graph_name]:
        print(i + " .")

def process(string,level,graph_name):
    global temp_statements
    org_string = string
    if org_string in triple_to_tripleId[graph_name]:
        return
    string = string[2:-2]
    string = string.strip()
    nesting = string.count('<<')
    if nesting == 0:
        if org_string not in triple_to_tripleId[graph_name]:
            triple_id = 't'+str(len(tripleId_to_triple[graph_name]) + 1) 
            tripleId_to_triple[graph_name][triple_id] = org_string
            triple_to_tripleId[graph_name][org_string] = triple_id
        else:
            triple_id = triple_to_tripleId[graph_name][org_string]

        values = string.split(' ')
        temp_statements.append(":"+triple_id + " subject " + values[0])
        temp_statements.append(":"+triple_id + " predicate " + values[1])
        temp_statements.append(":"+triple_id + " object " + values[2])


    else:

        
        starting_index = string.find("<<")
        ending_index = string.rfind(">>")


        if starting_index==0 and ending_index!=(len(string)-2):
            # only subject is nested
            # << >> :b :c

            index1 = -1
            index2 = -1
            temp = []
            for i in range(len(string)):
                if(string[i]==':'):
                    temp.append(i)

            index1 = temp[-2]
            index2 = temp[-1]

            subject = string[:index1-1]
            predicate = string[index1:index2-1]
            object = string[index2:]

            process(subject,level+1,graph_name)

            if org_string not in triple_to_tripleId[graph_name]:            
                triple_id = 't'+str(len(tripleId_to_triple[graph_name])+1) 
                tripleId_to_triple[graph_name][triple_id] = org_string
                triple_to_tripleId[graph_name][org_string] = triple_id
            else:
                triple_id = triple_to_tripleId[graph_name][org_string]


            if level > 1:
                temp_statements.append(":"+triple_to_tripleId[graph_name][subject] + " " + predicate + " "  + object  )
                temp_statements.append(":"+triple_id + " subject " + ":"+triple_to_tripleId[graph_name][subject])
                temp_statements.append(":"+triple_id + " predicate " + predicate)
                temp_statements.append(":"+triple_id + " object " + object)

            else:
                temp_statements.append(":"+triple_to_tripleId[graph_name][subject] + " " + predicate + " "  + object  )




        elif starting_index!=0 and ending_index==(len(string)-2):
            # only object is nested
            # :a :b << >>


            index1 = -1
            index2 = -1
            temp = []
            for i in range(len(string)):
                if(string[i]==':'):
                    temp.append(i)

            index1 = temp[0]
            index2 = temp[1]


            subject = string[index1:index2-1]
            predicate = string[index2:string.find("<",index2)-1]
            object = string[string.find("<",index2):]


            process(object,level+1,graph_name)

            
            triple_id = 't'+str(len(tripleId_to_triple[graph_name]) + 1) 
            tripleId_to_triple[graph_name][triple_id] = org_string
            triple_to_tripleId[graph_name][org_string] = triple_id


            if level > 1:
                temp_statements.append(subject + " " + predicate + " "  + ":"+triple_to_tripleId[graph_name][object]  )
                temp_statements.append(":"+triple_id + " subject " + subject)
                temp_statements.append(":"+triple_id + " predicate " + predicate)
                temp_statements.append(":"+triple_id + " object " + ":"+triple_to_tripleId[graph_name][object])

            else:
                temp_statements.append(subject + " " + predicate + " "  + ":"+triple_to_tripleId[graph_name][object]  )








        elif starting_index==0 and ending_index==(len(string)-2):
            # both are nested
            # << >> :b << >> 


            temp = []
            index1 = -1
            index2 = -1
            sum = 0
            for i in range(len(string)):
                if string[i]=='<':
                    sum+=1
                elif string[i]=='>':
                    sum-=1
                    if(sum==0):
                        temp.append(i)

            # print(temp)
            
            index1 = temp[0]
            index2 = temp[1]


            subject = string[:index1+1]
            predicate = string[string.find(":",index1):string.find("<",index1)-1]
            object = string[string.find("<",index1):]


            process(subject,level+1,graph_name)
            process(object,level+1,graph_name)

            
            triple_id = 't'+str(len(tripleId_to_triple[graph_name]) + 1) 
            tripleId_to_triple[graph_name][triple_id] = org_string
            triple_to_tripleId[graph_name][org_string] = triple_id


            if level > 1:
                temp_statements.append(":"+triple_to_tripleId[graph_name][subject] + " " + predicate + " "  + ":"+triple_to_tripleId[graph_name][object]  )
                temp_statements.append(":"+triple_id + " subject " + ":"+triple_to_tripleId[graph_name][subject])
                temp_statements.append(":"+triple_id + " predicate " + predicate)
                temp_statements.append(":"+triple_id + " object " + ":"+triple_to_tripleId[graph_name][object])

            else:
                temp_statements.append(":"+triple_to_tripleId[graph_name][subject] + " " + predicate + " "  + ":"+triple_to_tripleId[graph_name][object]  )



def process_nquad(nquad_string):
    graph_name = nquad_string[1 + nquad_string.rfind(':'):-2]
    triple_part = nquad_string[:nquad_string.rfind(':')].strip() + " >>"
    process_ntriple(triple_part, graph_name)
    


run = True
while run:
    print("\n\n\nSelect one of the options ->")
    print("0) To quit press 0")
    print("1) To insert N-Triple press 1")
    print("2) To get all statements in graph press 2")
    print("3) To insert N-quad press 3")

    ch = input()

    if ch=="1":
        print("Enter graph name")
        graph_name = input()
        print("Enter N-triple")
        triple_string = input()
        triple_string = "<< " + triple_string + " >>"
        process_ntriple(triple_string, graph_name)
    elif ch=="2":
        print("Enter graph name")
        graph_name = input()
        print_statements(graph_name)
    elif ch=="3":
        print("Enter N-quad")
        quad_string = input()
        quad_string = "<< "  + quad_string + " >>"
        process_nquad(quad_string)
        
    elif ch=="0":
        print("Quitting...")
        run = False
    else:
        print("invalid command")











