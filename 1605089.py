import numpy as np
from pprint import pprint
import copy
consistency_check = 0
failure = 0 
class Variable:
    domain = set()
    
    def __init__(self,value,row,column,ddeg,sdeg):
        self.value = value
        self.row = row
        self.column = column
        self.ddeg = ddeg
        self.sdeg = sdeg

    def set_value(self, value):
        self.value = value
    def set_row(self, row):
        self.row = row
    def set_column(self, column):
        self.column = column
    def set_ddeg(self, ddeg):
        self.ddeg = ddeg
    def set_sdeg(self, sdeg):
        self.sdeg = sdeg
    def set_domain(self, domain):
        self.domain = domain

    def get_value(self):
        return self.value
    def get_row(self):
        return self.row
    def get_column(self):
        return self.column
    def get_ddeg(self):
        return self.ddeg
    def get_sdeg(self):
        return self.sdeg
    def get_domain(self):
        return self.domain
    

def read_file(filename):

    f = open("D:\\google drive\\3-2\\cse 318\\Offlines\\offline 4\\csp_task\\data\\"+filename+".txt", "r")
    x = f.read()
    x = x.replace('start=','')
    y = x[x.index('['):x.index(']')+len(']')]
    y = y.replace('|', '')
    y = y.replace(" ", "")
    y = y.replace('[', '')
    y = y.replace(']', '')
    y = y[1:]
    print(y)
    a = np.array([[int(j) for j in i.split(',')] for i in y.splitlines()])
    f.close()
    return len(a),a

def printv(v, N):
    t = [[[] for i in range(N)] for j in range(N)]
    r = set()
    c = set ()

    for i in range(0,N):
        for j in range(0,N):
            t[i][j] = v[i][j].get_value()
            r.add(v[i][j].get_value())
            c.add(v[i][j].get_value())
           
    if len(r)== N and len(c)==N:
        print("valid!!")
    print(t)


def updateDomainAndDeg(v,u, N):
    u.clear()
    for i in range(0,N):
        for j in range(0,N):
            dom = set()
            deg = 0
           
            if (v[i][j].get_value())==0:
               
                dom2=set()
                for k in range(0,N):
                    if v[v[i][j].get_row()][k].get_value() == 0:
                        #continue
                        deg = deg + 1
                    else:
                        dom2.add(v[v[i][j].get_row()][k].get_value())
                for k in range(0,N):
                    if v[k][v[i][j].get_column()].get_value() == 0:
                        #continue
                        deg = deg + 1
                    else:
                        dom2.add(v[k][v[i][j].get_column()].get_value())
                for k in range(0,N):
                    if k+1 in dom2:
                        continue
                    else:
                        dom.add(k+1)
                v[i][j].set_domain(dom)
                v[i][j].set_ddeg(deg) 
                u.append(v[i][j])

    
 
def FC(v,uc, N,t):
    global consistency_check, failure
    u = copy.copy(uc)
    if(len(u)==0):
        #print("\n")

        printv(v,N)
        print("cc and failure: ")
        print(consistency_check,failure)
        # del cc
        # del f
        # del u
        return True
    if t==1:
        #print(cc)
        u =  sorted(u, key=lambda x: len(x.get_domain()), reverse=True)
        
    if t==2:
        
        u = sorted(u, key=lambda x: x.get_ddeg())
        
    if t==3:
        u = sorted(u, key=lambda x: (len(x.get_domain()),-x.get_ddeg()), reverse=True )
       
    if t == 4:
        #print("kokhon khay?")
        u = sorted(u, key=lambda x: float((len(x.get_domain())/x.get_ddeg())),reverse=True)
        
    if t == 5:
        u = sorted(u, key=lambda x: x.get_ddeg(), reverse=True)
   
    u1 = u.pop()
    #print(len(u))
    
    for i in u1.get_domain():
       # print(i)
        #u1.set_value(i)
        consistency_check= consistency_check+1
       # print(consistency_check)
        v[u1.get_row()][u1.get_column()].set_value(i)
        updateDomainAndDeg(v,u,N)

        result = FC(v,u,N,t)
        if result== True:
            return result

        #u1.set_value(0)
        failure = failure+1
        #cc = cc+1
        v[u1.get_row()][u1.get_column()].set_value(0)
        updateDomainAndDeg(v,u,N)
    
    
    return False

        


if __name__=="__main__":

    # global consistency_check, failure
    N,initlatin = read_file('d-10-01.txt')
    var = [[[] for i in range(N)] for j in range(N)] # initialized 2d array
    
    for i in range(0,len(initlatin),1):
        for j in range(0,len(initlatin),1):
            var[i][j] = Variable(initlatin[i][j],i,j,None,2*(N-1))

   # print(initlatin)
    
    #SETTING DYNAMIC DEGREE
    for i in range(0,N):
        for j in range(0,N):
            deg = 0
            for k in range(0,N):
                
                if var[var[i][j].get_row()][k].get_value() == 0:
                    deg = deg + 1
                if var[k][var[i][j].get_column()].get_value() == 0:
                    deg = deg + 1
            var[i][j].set_ddeg(deg) 
    
    #SETTING DOMAIN FOR EVERY VARIABLE
    for i in range(0,N):
        for j in range(0,N):
            dom = set()
           
            if (var[i][j].get_value())==0:
                
                dom2=set()
                for k in range(0,N):
                    if var[var[i][j].get_row()][k].get_value() == 0:
                        continue
                    else:
                        dom2.add(var[var[i][j].get_row()][k].get_value())
                for k in range(0,N):
                    if var[k][var[i][j].get_column()].get_value() == 0:
                        continue
                    else:
                        dom2.add(var[k][var[i][j].get_column()].get_value())
                for k in range(0,N):
                    if k+1 in dom2:
                        continue
                    else:
                        dom.add(k+1)

                
            # else:
        
            #     dom.add(var[i][j].get_value())
            # # print(dom)
            var[i][j].set_domain(dom)

   # unassvar = set()
    unassvar = []
    for i in range(0,N):
        for j in range(0,N):
            if var[i][j].get_value() == 0:
                    unassvar.append(copy.copy(var[i][j]))
    
    # for i in range(0, len(unassvar)):
    #     print(unassvar[i].get_value(), unassvar[i].get_domain(), unassvar[i].get_ddeg())

    print("1 for SMALLEST DOMAIN FIRST\n 2 for MAXIMUM DYNAMIC DEGREE\n 3 for BRELUZ\n 4 for DOMtodDEG\n 5 for MINIMUM DYNAMIC DEGREE\n 0 for RANDOM\n")

    
    h = int(input("Enter the heuristic number:")) 
    
    consistency_check = 0
    failure = 0 
    print("Entered value " + str(h))
    FC(var,unassvar,N,h)
    
   