import matplotlib.pyplot as plt
import numpy as np
from plainbox.impl.pod import POD
from sklearn import neighbors, datasets



#a = [1,2,2,2,2,6,0,0,0,0,9,9,9]
#b = [0,0,0,1,1,1,2,2,2,2,5,5,5]

#print(np.copy(a))
#print(np.argmax(np.bincount(b,a)))

iris = datasets.load_iris()
X = iris.data[:,:2]
y = iris.target

#print(iris)
#print(X)

print(len(iris.data[0]))
for i in range(0,len(iris.data[0])):
    print(iris.feature_names[i])
for i in range(0,len(iris.data)):
    s = ""
    for k in range(0,len(iris.data[0])):
        s = s+str(iris.data[i][k])+" "
    s = s+str(iris.target[i])
    print(s)




#a = [0,1,2,3,11,5,6,7,8,9,10]

#a = np.delete(a,3)

#print(a)

def ONN(X,y,u):
    """Classifies by the nearest training object

    Keyword arguments:
    X -- training sample
    y -- classes of training samples
    u -- object to classify
    """
    return y[np.argmin([(x[0]-u[0])**2 + (x[1]-u[1])**2 for x in X])]

def KNN(X,y,u,k):
    """Classifies by K nearest training object

    Keyword arguments:
    X -- training sample
    y -- classes of training samples
    u -- object to classify
    k -- number of near object to classify
    """
    L = [(x[0]-u[0])**2 + (x[1]-u[1])**2 for x in X]
    L,y = zip(*sorted(zip(L, y)))
    l = []
    for i in range(0,k):
        l.append(y[i])
    u, c = np.unique(l, return_counts=True)
    return u[np.argmax(c)]


def LOOforKNN(X,y):
    diff = len(X)
    gk = 0
    kvarray = []
    u = [[],0]
    for k in range(1,len(X)):
        cd = 0
        for i in range(1,len(X)):
            u[0] = X[i]
            u[1] = y[i]
            Xt = np.delete(X,i,0)
            yt = np.delete(y,i)
            if(KNN(Xt,yt,u[0],k)!=u[1]):
                cd = cd+1
        if(diff>cd):
            diff = cd
            gk = k
        kvarray.append(cd)
    return gk,kvarray

def ParsenWindow(X,y,K,h,u):
    P = [K(((x[0]-u[0])**2 + (x[1]-u[1])**2)/h,1) for x in X]
    return np.argmax(np.bincount(y,P))


def PotentiaFunctions(X, y, K, h, t, u):
    P = []
    for i in range(0, len(X)):
        P.append(t[i]*K(((X[i][0] - u[0]) ** 2 + (X[i][1] - u[1]) ** 2) / h[i], 1))
    return np.argmax(np.bincount(y, P))


def GetHForPotentialFunctions(X, y, p):
    diff = 1
    u = [[], 0]
    t = [0 for x in X]
    h = [1 for x in X]
    while(diff>p):
        cd = 0
        for i in range(1, len(X)):
            u[0] = X[i]
            u[1] = y[i]
            Xt = np.delete(X, i, 0)
            yt = np.delete(y, i)
            if (PotentiaFunctions(Xt, yt, K, h,t, u[0]) != u[1]):
                cd = cd + 1
                t[i] = t[i]+1
            else:
                print(str(PotentiaFunctions(Xt, yt, K, h,t, u[0]))+" "+str(u[1]))
        diff = cd/len(X)
        print(str(diff*10)+"%")

    return h,t

def K(x,l):
    if(x>l):
        return 0;
    else:
        return (l-x)/l;


#h = GetHForPotentialFunctions(X,y,0.1)
#print(h)
#gk,ga = LOOforKNN(X,y)
#print(gk)

#plt.plot([x for x in range(1,len(X))], ga, 'ro')
#plt.axis([0, len(X)+1, 0, ga[np.argmax(ga)]+1])
#plt.show()