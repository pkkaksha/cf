import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Read the Ratings
def training():
    Q=np.zeros(shape=(944,1683))
    f = open('/home/pshall/Desktop/sem_project/ml-100k/u2.base', 'r')
    for line in f:
        my_list = line.split("\t")
        Q[int(my_list[0])][int(my_list[1])]=float(my_list[2])


    # If the Rating is more than 3 then make is 1 else 0
    Q = Q>3
    Q[Q == True] = 1
    Q[Q == False] = 0
    # To be consistent with our Q matrix
    Q = Q.astype(np.float64, copy=False)
    W = np.zeros(shape=(944,1683))

    # set user Oreinted Weighting
    for i in range(1,944):
        count=0
        for j in range(1,1683):
            if(Q[i][j]>0):
                count=count+1
        weight=1-(float(count)/1683)
        for j in range(1,1683):
            if(Q[i][j]>0):
                W[i][j]=1
            else:
                W[i][j]=weight/10
    # Definfing Parameters
    lambda_ = 0.05
    n_factors =20
    m, n = Q.shape
    n_iterations =1
    num_of_retrieve=10


    # random initiliase Factor  matrix
    X = np.random.rand(m, n_factors)
    Y = np.random.rand(n_factors, n)


    # calculate error
    def get_error(Q, X, Y, W):
        return np.sum((W * (Q - np.dot(X, Y)))**2)

    #Als for finding X and Y
    weighted_errors = []
    for ii in range(n_iterations):
        #print ii
        for u, Wu in enumerate(W):
            X[u] = np.linalg.solve(np.dot(Y, np.dot(np.diag(Wu), Y.T)) + lambda_ * np.eye(n_factors),
                                   np.dot(Y, np.dot(np.diag(Wu), Q[u].T))).T

        for i, Wi in enumerate(W.T):

            Y[:,i] = np.linalg.solve(np.dot(X.T, np.dot(np.diag(Wi), X)) + lambda_ * np.eye(n_factors),
                                     np.dot(X.T, np.dot(np.diag(Wi), Q[:, i])))
        weighted_errors.append(get_error(Q, X, Y, W))
        #print "the error now is "
        #print get_error(Q,X,Y,W)
        #print('{}th iteration is completed'.format(ii))

    # final Rating matrix
    Q_hat = np.dot(X,Y)

    #for i in range(1,1683):
    #   print Q_hat[1][i]

    top_recommandation=[] #all new recommandations Rating
    for i in range(944):
        top_recommandation.append([])
        for j in range(1683):
            if((Q[i][j]==1.0)):
                pass
            else:
                top_recommandation[i].append((Q_hat[i][j], j))
    Result_top_ten=[]
    Test_list=[]
    Average_precision=[]
    # Read the new Test recommandatio for user
    f2 = open('/home/pshall/Desktop/sem_project/ml-100k/u2.test', 'r')
    for i in range(0,944):
        Test_list.append([])
        Average_precision.append([])
        Result_top_ten.append([])
    for line in f2:
        my_list = line.split("\t")
        if((int(my_list[2]))>0):
           # print len(Test_list[int(my_list[0])])
            Test_list[int(my_list[0])].append(int(my_list[1]))


    for i in range(1,944):
        top_recommandation[i]=sorted(top_recommandation[i],key=lambda top_recommandation:top_recommandation[0],reverse=True)
        top_recommandation[i]=top_recommandation[i][:num_of_retrieve]
        for j in range(num_of_retrieve):
            x=top_recommandation[i][j]
            Result_top_ten[i].append(x[1])
    # print top_recommandation[2]

    # title=[]

    # for i in top_recommandation[2]:
    #   #print i[1]
    #   title.append(i[1])

    f1=open('/home/pshall/Desktop/sem_project/ml-100k/u.item','r')
    title_res=[]
    dict_title={}
    revdic_title={}
    for i in f1:
        k=str(i).split("|")
        dict_title[k[0]]=k[1]
    #print dict_title.keys()    
        #revdic_title[k[1]]=k[0]
    # print "Movie-id","Movie-Name"
    # for i in title:
    #   print i,dict_title[str(i)]

    # for i in f1:
    #     k=str(i).split("|")
    #     revdic_title[k[1]]=k[0]

    title_final=[]
    for i in range(1,944):
        title1=[]
        for j in range(len(top_recommandation[i])):
            title1.append(top_recommandation[i][j])
        title_final.append(title1)


    # print "size",len(title_final)

    # for i in range(0,len(title_final)):
    #     print str(i+1)+"user"
    #     for j in range(len(title_final[i])):
    #         print title_final[i][j][1]

    dict_finalres={}
    for i in range(0,len(title_final)):
        list1=[]
        for j in range(len(title_final[i])):
            if str(title_final[i][j][1]) in dict_title.keys():
                list1.append((str(title_final[i][j][1]),dict_title[str(title_final[i][j][1])]))
            #else:
                #print "Fail"
                #print i,j,title_final[i][j][1],type(title_final[i][j][1])
        dict_finalres[i+1]=list1
    # print dict_finalres.keys()
    # for key in dict_finalres.keys():
    #      print key,dict_finalres[key]
    

    mean_average_precision=0.0
    Average_precision_sum=0
    Average_recall=0.0
    mean_average_recall=0.0
    total_count=0
    for user in range(1,944):
        if(len(Test_list[user])>1):
            total_count=total_count+1
            count = 0
            sum = 0.0
            num_of_recommanded=0
            item = Result_top_ten[user]
            for i in range(num_of_retrieve):
                if (item[i] in Test_list[user]):
                    num_of_recommanded=num_of_recommanded+1
                    count=count+1
            Average_precision_sum=Average_precision_sum+(float(num_of_recommanded))/num_of_retrieve
            Average_recall=Average_recall+float(num_of_recommanded)/len(Test_list[user])

    mean_average_recall=Average_recall/total_count
    mean_average_precision=(Average_precision_sum)/total_count

    print "mean average precision is",mean_average_precision
    print "mean average recall is",mean_average_recall
    return dict_finalres
    #print mean_average_precision
    #print mean_average_recall
    """
    count=0;
    for user in range(1,944):
        if(((Average_precision[user]))>1):
            #print "for user"
            #print user
            #print Average_precision[user]
            count=count+1
            x=Average_precision[user]
            mean_average_precision = mean_average_precision + x[0]
"""
