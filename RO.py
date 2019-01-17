"""
learn from xprog and bertsimas's paper(price of robustness)
http://xprog.weebly.com/
the initial model cann't be solved by gurobi or cplex
the problem has an equivalent linear formulation as follows:
    max  z
    s.t. z<=sum(p[i]x[i])-(sum(Q[i])+Γ[i]m[i])
        Q[i]+m[i]>=σ[i]x[i]
        Q[i]>=0
        m[i]>=0
        sum(x[i])=1
        x[i]>=0
Γis the protection level of the actual portfolio return in the following sense

"""
from gurobipy import *

try:
    m = Model("RO")
#establishment of constant
    σ = []
    p = []
    Γ= []
    for n in range(1,151):
        σ.append(0.05/450*(2*n*150*151)**0.5)
        p.append(1.15+n*0.05/150)
        Γ.append(5)
#Add variables
    x = m.addVars(150,lb=0,name='x')
    z = m.addVar(name='z')
    Q = m.addVars(150,name='Q')
    mm = m.addVars(150,name='m')

    px = sum(p[i]*x[i] for i in range(150))
    QC =sum(Q[i] for i in range(150))

# Add Constrs
    m.addConstrs((z<=px-mm[i]*Γ[i]-QC for i in range(150)),name='first')
    m.addConstrs((mm[i]+Q[i]>=σ[i]*x[i] for i in range(150)),name='second')
    m.addConstr(sum(x[i] for i in range(150))==1,name='third')
#set obj
    m.setObjective(z,GRB.MAXIMIZE)

#print model
    m.write ("RO.lp")
#solve model
    m.optimize()
#print variables
    # for v in m.getVars ():
    #     print ('%s %g' % (v.varName, v.x))

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')