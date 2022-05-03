from argon2 import PasswordHasher
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF


# g = Graph()
# g.bind("foaf", FOAF)

# print(g)

# bob = URIRef("http://example.org/people/Bob")
# g.add((bob, RDF.type, FOAF.Person))
# g.add((bob, FOAF.name, Literal("Bob")))
# g.add((bob, FOAF.age, Literal(38)))

# import pprint
# for stmt in g:
#     pprint.pprint(stmt)


statements = []

tripleId_to_triple = {}
triple_to_tripleId = {}
cnt = 0

bcnt = 0


def print_statements(input_string):
    global statements,triple_to_tripleId,tripleId_to_triple,cnt
    statements = []
    tripleId_to_triple = {}
    triple_to_tripleId = {}
    cnt = 0
    bcnt = 0
    process(input_string,1)
    for i in statements:
        print(i)

    print("\n\n\n")

def process(string,level):
    global cnt
    

    org_string = string
    


    string = string[2:-2]
    string = string.strip()
    nesting = string.count('<<')
    if nesting == 0:
        cnt+=1
        triple_id = 't'+str(cnt) 
        tripleId_to_triple[triple_id] = org_string
        triple_to_tripleId[org_string] = triple_id

        values = string.split(' ')
        statements.append(triple_id + " subject " + values[0])
        statements.append(triple_id + " predicate " + values[1])
        statements.append(triple_id + " object " + values[2])


    else:

        


        starting_index = string.find("<<")
        ending_index = string.rfind(">>")

        # print(string)
        # print(starting_index)
        # print(ending_index)
        # print(len(string)-2)

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

            process(subject,level+1)

            cnt+=1
            triple_id = 't'+str(cnt) 
            tripleId_to_triple[triple_id] = org_string
            triple_to_tripleId[org_string] = triple_id


            if level > 1:
                statements.append(triple_to_tripleId[subject] + " " + predicate + " "  + object  )
                statements.append(triple_id + " subject " + triple_to_tripleId[subject])
                statements.append(triple_id + " predicate " + predicate)
                statements.append(triple_id + " object " + object)

            else:
                # statements.append(triple_to_tripleId[subject] + " " + values[1] + " "  + values[2]  )
                statements.append(triple_to_tripleId[subject] + " " + predicate + " "  + object  )




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


            process(object,level+1)

            cnt+=1
            triple_id = 't'+str(cnt) 
            tripleId_to_triple[triple_id] = org_string
            triple_to_tripleId[org_string] = triple_id


            if level > 1:
                statements.append(subject + " " + predicate + " "  + triple_to_tripleId[object]  )
                statements.append(triple_id + " subject " + subject)
                statements.append(triple_id + " predicate " + predicate)
                statements.append(triple_id + " object " + triple_to_tripleId[object])

            else:
                # statements.append(triple_to_tripleId[subject] + " " + values[1] + " "  + values[2]  )
                statements.append(subject + " " + predicate + " "  + triple_to_tripleId[object]  )








        elif starting_index==0 and ending_index==(len(string)-2):
            # both are nested
            # << >> :b << >> 


            # print("here")
            # print(string)
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


            process(subject,level+1)
            process(object,level+1)

            cnt+=1
            triple_id = 't'+str(cnt) 
            tripleId_to_triple[triple_id] = org_string
            triple_to_tripleId[org_string] = triple_id


            if level > 1:
                statements.append(triple_to_tripleId[subject] + " " + predicate + " "  + triple_to_tripleId[object]  )
                statements.append(triple_id + " subject " + triple_to_tripleId[subject])
                statements.append(triple_id + " predicate " + predicate)
                statements.append(triple_id + " object " + triple_to_tripleId[object])

            else:
                # statements.append(triple_to_tripleId[subject] + " " + values[1] + " "  + values[2]  )
                statements.append(triple_to_tripleId[subject] + " " + predicate + " "  + triple_to_tripleId[object]  )


            # print("subject = ",subject,len(subject))
            # print("predicate = ",predicate,len(predicate))
            # print("object = ",object,len(object))




            # print("ERROR")



        # values = []
        # subject = string[string.find('<<') + 2:string.rfind('>>')].strip()
        # rest = string[string.rfind('>>') + 2:].strip().split(' ')
        # print(string[string.rfind('>>') + 2:])
        # print("rest = ",rest)
        # values.append(subject)

        # values+=rest
        # process("<<" + subject + ">>",level+1)

        # cnt+=1
        # triple_id = 't'+str(cnt) 
        # tripleId_to_triple[triple_id] = string
        # triple_to_tripleId[string] = triple_id


        # if level > 1:
        #     statements.append(triple_to_tripleId[subject] + " " + values[1] + " "  + values[2]  )
        #     statements.append(triple_id + " subject " + triple_to_tripleId[subject])
        #     statements.append(triple_id + " predicate " + values[1])
        #     statements.append(triple_id + " object " + values[2])

        # else:
        #     statements.append(triple_to_tripleId[subject] + " " + values[1] + " "  + values[2]  )

    # print(string)




input_string1 = '<< :a :name "Alice" >>'
input_string2 = '<< << :a :name "Alice" >> :reportedBy :charlie >>'
input_string3 = '<< << << :a :name "Alice" >> :reportedBy :charlie >> :thoughtBy :bob >>'
input_string4 = '<< << << << :a :name "Alice" >> :reportedBy :charlie >> :thoughtBy :bob >> :writtenBy :mary >>'
input_string5 = '<< << :ram :created << :ram :is "Great" >> >> :saidBy :mary >>'
input_string6 = '<< :charlie :reported << :a :name "Alice" >> >>'

input_string7 = '<< << :a :name "Alice" >> :reportedBy << :b :name "Bob" >> >>'

# print_statements(input_string1)
# print_statements(input_string2)
# print_statements(input_string3)
# print_statements(input_string4)
# print_statements(input_string5)
# print_statements(input_string6)
print_statements(input_string7)









