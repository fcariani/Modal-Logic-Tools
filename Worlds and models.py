# libraries

from copy import deepcopy

# symbols

dottedbar = u'\u250b'
ubox = u'\u2610'
udiamond = u'\u2b26'
bot = u'\u22a5'
 
# language
atomics = ['p', 'q', 'r', bot]
connectives = ['&', 'v', '~', '>', ubox, udiamond]
binary_connectives = ['&', 'v', '>']
unary_connectives = ['~', ubox, udiamond]
primitive = [bot,'>','N']
parentheses = ['(', ')']

class binary:
    def __init__(self, x1, x2, conn):
        self.x1 = x1
        self.x2 = x2
        self.conn = conn
    def first_arg(self):
        return self.x1
    def second_arg(self):
        return self.x2
    def connective(self):
        return self.conn
    def __str__(self):
        return '('+str(self.x1)+ ' ' + self.conn + ' ' + str(self.x2) + ')'

class disj(binary):
    def __init__(self, x1, x2):
        super().__init__(x1,x2,'v')

class conj(binary):
    def __init__(self, c1, c2):
        super().__init__(c1,c2,'&')

class cond(binary):
    def __init__(self, a1, c2):
        super().__init__(a1,c2,'>')

class unary:
    def __init__(self, x1, conn):
        self.x1 = x1
        self.conn = conn
    def argument(self):
        return self.x1
    def connective(self):
        return self.conn
    def __str__(self):
        return '(' + self.conn + str(self.x1) + ')'

class neg(unary):
    def __init__(self, x1):
        super().__init__(x1, '~')

class box(unary):
    def __init__(self, x1):
        super().__init__(x1, ubox)
        self.x1 = x1

class diamond(unary):
    def __init__(self,x1):
        super().__init__(x1, udiamond)

################### WORLDS class

class world:
    def __init__(self, p, q, r, name ='world'):
        self.p = p
        self.q = q
        self.r = r
        self.pl = 'p'
        self.ql = 'q'
        self.rl = 'r'
        self.name = name
    def atoms_value(self, atom, val):
        if val:
            return '  ' + atom +' '
        else:
            return str(neg(atom))
    def display(self):
        print(self.name, end=": |")
        print(self.atoms_value(self.pl, self.p), end="|")
        print(self.atoms_value(self.ql, self.q), end="|")
        print(self.atoms_value(self.rl, self.r), end="|")
        print("\n")
    def __repr__(self):
        return(self.name + ": |" + self.atoms_value(self.pl, self.p) + " | " 
               + self.atoms_value(self.ql, self.q) + "|" +
               self.atoms_value(self.rl, self.r) + "|" + "\n")

################### MODELS class

        
         # we implement accessibility relations as dictionaries
        # relating each world to a set
class model:
    def __init__(self, worlds, relation = None):
        self.worlds = set(worlds)
        self.relation = relation
        if self.relation == None:
            self.relation = {}
            for w in self.worlds:
                self.relation[w] = (deepcopy(set()))
    def add_world(self, w):
        self.worlds.add(w)
    def add_link(self, w1, w2):
        self.relation[w1].add(w2)
    def link_all_to(self, w1):
        for w in self.worlds:
            self.add_link(w, w1)
    def link_to_all(self, w1):
        for w in self.worlds:
            self.add_link(w1, w)
    # add procedures for removing worlds and links
    def relates_to(self, w):
        return self.relation[w]
    # some procedures to operate on the relation globally
    def make_reflexive(self):
        for w in self.worlds:
            self.add_link(w, w)
    def check_reflexive(self):
        answer = True
        for w in self.worlds:
            answer = answer and (w in self.relation[w])
        return answer 
    def make_symmetric(self):
        for w in self.worlds:
            for v in self.worlds:
                if v in self.relation[w]:
                     self.add_link(v, w)
    def check_symmetric(self):
        answer = True
        for w in self.worlds:
            for v in self.worlds:
                if v in self.relation[w]:
                    answer = answer and (w in self.relation[v])
        return answer 
    def check_transitive(self):
        answer = True
        for w in self.worlds:
            for v in self.worlds:
                for z in self.worlds:
                    if v in self.relation[w] and z in self.relation[v]:
                        answer = answer and (z in self.relation[w]) 
        return answer 
    def make_transitive_step(self):
        for w in self.worlds:
            for v in self.worlds:
                for z in self.worlds:
                    if v in self.relation[ w] and z in self.relation[v]:                        
                        self.add_link(w, z) 
    def make_transitive(self):  # in general, one application of make-transitive step, won't suffice
        while self.check_transitive() == False: # so we iterate until the model is transitive. 
            self.make_transitive_step()
    def check_euclidean(self):
        answer = True
        for w in self.worlds:
            for v in self.worlds:
                for z in self.worlds:
                    if v in self.relation[w] and z in self.relation[w]:
                        answer = answer and (z in self.relation[v]) 
        return answer 
    def make_euclidean_step(self):
        for w in self.worlds:
            for v in self.worlds:
                for z in self.worlds:
                    if v in self.relation[w] and z in self.relation[w]:                       
                        self.add_link(v, z)  
                        self.add_link(z, v)  
    def make_euclidean(self):  # in general, one application of make-transitive step, won't suffice
        while self.check_euclidean() == False: # so we iterate until the model is transitive. 
            self.make_euclidean_step()
    def check_serial(self):
        answer = True
        for w in self.worlds:
            answer = answer and (self.relation[w]!= set())
        return answer
    def display(self):
        sorted_worlds = sorted(self.worlds, key= lambda world: world.name)
        print('----------------------------------------------------')
        print('truth-values at worlds') 
        print('----------------------------------------------------')
        for w in sorted_worlds:
            w.display()
        print('----------------------------------------------------')
        print('relation (lists the worlds that each world accesses)')
        print('----------------------------------------------------')
        for w in sorted_worlds:
            print(w.name, end=": ")
            for v in self.relation[w]:
            # for v in sorted(self.relation[w], key= lambda world: world.name):
                print(v.name, end=" ")
            print('\n')
    def display_extended(self):
        sorted_worlds = sorted(self.worlds, key= lambda world: world.name)
        print('----------------------------------------------------')
        print('truth-values at worlds') 
        print('----------------------------------------------------')
        for w in sorted_worlds:
            w.display()
        print('----------------------------------------------------')
        print('relation (lists the worlds that each world accesses)')
        print('----------------------------------------------------')
        for w in sorted_worlds:
            print(w.name, end=": ")
            for v in self.relation[w]:
            # for v in sorted(self.relation[w], key= lambda world: world.name):
                print(v.name, end=" ")
            print('\n')
        print('----------------------------------------------------')
        print('properties')
        print('----------------------------------------------------')
        print('Reflexive? ' + str(self.check_reflexive() ))
        print('Symmetric? ' + str(self.check_symmetric() ))
        print('Transitive? ' + str(self.check_transitive() ))

# this is the semantic evaluation function 

def true_at(A, w, M):# A is our sentence, w is a world, M is a model
    if A in atomics:
        if A == 'p':
            return w.p
        if A == 'q':
            return w.q
        if A == 'r':
            return w.r
        if A == bot:
            return False
    elif A.connective()=='&':
        return true_at(A.first_arg(), w, M) and true_at(A.second_arg(), w, M)
    elif A.connective()=='v':
        return true_at(A.first_arg(), w, M) or true_at(A.second_arg(), w, M)
    elif A.connective()=='>':
        return not true_at(A.first_arg(), w, M) or true_at(A.second_arg(), w, M)
    elif A.connective()=='~':
        return not true_at(A.argument(), w, M)
    elif A.connective()==ubox:
        state = True
        for x in M.relates_to(w):
            state = state and true_at(A.argument(), x, M)
        return state
    elif A.connective()==udiamond:
        state = False
        for x in M.relates_to(w):
            state = state or true_at(A.argument(), x, M) 
        return state   

def true_everywhere(A, M):
    state = True
    for w in M.worlds:
        state = state and true_at(A, w, M)
    return state

def true_everywhere_list(list, M):
    state = True
    for A in list:
        state = state and true_everywhere(A, M)
    return state

def true_somewhere_list(lst, M):
    witness_worlds = [] # this variable will store all of the worlds at which the list is true
    for w in M.worlds:
        liststate = True
        for A in lst:
            liststate = liststate and true_at(A,w,M)
        if liststate:
            witness_worlds += [w] 
    return witness_worlds

def is_counterexample_q(prem, concl, M):
    if true_somewhere_list(prem+[neg(concl)],M)!=[]:
        return True

def is_counterexample_question(prem, concl, M):
    if true_somewhere_list(prem+[neg(concl)],M)!=[]:
        print('this model is a counterexample to the argument\'s validity')
        M.display()
        print('In particular, the premises are true and the conclusion false at worlds: ', end="")
        for w in true_somewhere_list(prem+[neg(concl)],M):
            print(str(w.name), end=",")
        print('\n')
    else:
        print('this model is not a counterexample to the argument\'s validity (but the argument may yet be invalid)')