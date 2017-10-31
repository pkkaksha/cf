import numpy
import random
def training1():
    numOfItem=3953
    numOfUser=6041
    numOfnegative=[]
    num_of_retrieve=10
    numOfFaeture=2
    steps=1
    valueofK=3
    Ratings=numpy.zeros(shape=(numOfUser,numOfItem))
    newData=numpy.zeros(shape=(numOfUser,numOfItem))
    probability=numpy.zeros(shape=(numOfUser,numOfItem))
    release_date=[]
    last_movie_year=numpy.zeros(shape=(numOfUser))
    numofSecond=3600*24*365
    for i in range(numOfItem):
        release_date.append([])
        release_date[i].append(1995)
    for i in range(numOfUser):
        numOfnegative.append([])
        numOfnegative[i]=0

    def read_item_date():
        f = open('/home/pshall/Desktop/sem_project/time1.txt', 'r')
        for line in f:
            my_list = line.split("::")
            #print my_list
            release_date[int(my_list[0])][0]=int(my_list[1])
        #for i in range(numOfItem):
        #    print release_date[i]



    def readData():
        f = open('/home/pshall/Desktop/sem_project/train_80.txt', 'r')
        for line in f:
            my_list = line.split("::")
            u=int(my_list[0])
            i=int(my_list[1])
            r=int(my_list[2])
            t=int(my_list[3])
            if(r>=3):
                numOfnegative[u]=numOfnegative[u]+1
                Ratings[u][i] = 1
                newData[u][i] = 1
            if(last_movie_year[u]<t):
                last_movie_year[u]=t
        for i in range(numOfUser):
            last_movie_year[i]=int(last_movie_year[i]/numofSecond)+1+1970
            #print last_movie_year[i]
            #print i



    def find_probability_matrix():
        for u in range(1,numOfUser):
            total=0.0
            for i in range(1,numOfItem):
                if(Ratings[u][i]==1):
                    probability[u][i]=0
                else:
                    #1. probability[u][i]=1-(float(1)/(float(last_movie_year[u]+1)-(release_date[i][0])))
                    #2.if(last_movie_year[u]>release_date[i][0]):
                        #probability[u][i]=(float(last_movie_year[u])-(release_date[i][0]))
                    #else:
                        #probability[u][i]=0.5
                    if(last_movie_year[u]>release_date[i][0]):
                        x=(float(last_movie_year[u])-(release_date[i][0]))
                    else:
                        x=0.5
                    probability[u][i]=pow(x,0.33)
                total=total+probability[u][i]
            for i in range(1,numOfItem):
                probability[u][i]=(probability[u][i]/total)
        #for i in range(1, numOfItem):
            #print probability[1][i]




    def addNegativeExample():
        for u in range(1,numOfUser):
            l=[]
            k=[]
            for j in range(1,numOfItem):
                if(probability[u][j]>0):
                    l.append(j)
                    k.append(probability[u][j])
            if((numOfnegative[u]*valueofK)>=len(l)):
                Nonrated=len(l)
            else:
                Nonrated=numOfnegative[u]*valueofK

            mylist=numpy.random.choice(l, Nonrated, replace=False,p=k)
            for i in range(Nonrated):
                newData[u][int(mylist[i])]=1


    def matrix_factorization(R,newData, P, Q, K, alpha=0.0002, beta=0.02):
        Q = Q.T
        for step in xrange(steps):
            print step
            for i in xrange(len(R)):
                for j in xrange(len(R[i])):
                    if (newData[i][j]>0):
                        eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                        for k in xrange(K):
                            P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                            Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
            #eR = numpy.dot(P,Q)
            e = 0
            for i in xrange(len(R)):
                for j in xrange(len(R[i])):
                    if newData[i][j] > 0:
                        e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                        for k in xrange(K):
                            e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
            print e
            if e < 0.001:
                break
        return P, Q.T




    readData()
    read_item_date()
    find_probability_matrix()
    #print numOfnegative[1]

    addNegativeExample()
    N = numOfUser
    M = numOfItem
    P = numpy.random.rand(N,numOfFaeture)
    Q = numpy.random.rand(M,numOfFaeture)


    nP,nQ = matrix_factorization(Ratings,newData, P, Q, numOfFaeture)
    Q_hat=numpy.zeros(shape=(numOfUser,numOfItem))
    Q_hat = numpy.dot(nP, nQ.T)



    top_recommandation=[] #all new recommandations Rating
    for i in range(numOfUser):
        top_recommandation.append([])
        for j in range(numOfItem):
            if((newData[i][j]==1)):
                pass
            else:
                top_recommandation[i].append((Q_hat[i][j], j))
    Result_top_ten=[]
    Test_list=[]
    Average_precision=[]
    for i in range(0,numOfUser):
        Test_list.append([])
        Average_precision.append([])
        Result_top_ten.append([])

    f2 = open('/home/pshall/Desktop/sem_project/test_80.txt', 'r')

    for line in f2:
        my_list = line.split("::")
        if((int(my_list[2]))>0):
           # print len(Test_list[int(my_list[0])])
            Test_list[int(my_list[0])].append(int(my_list[1]))



    for i in range(1,numOfUser):
        top_recommandation[i]=sorted(top_recommandation[i],key=lambda top_recommandation:top_recommandation[0],reverse=True)
        top_recommandation[i]=top_recommandation[i][:num_of_retrieve]
        j=0
        while(j<num_of_retrieve and j<len(top_recommandation[i])):
            x=top_recommandation[i][j]
            Result_top_ten[i].append(x[1])
            j=j+1


    f1=open('/home/pshall/Desktop/sem_project/ml-100k/u.item','r')
    title_res=[]
    dict_title={}
    revdic_title={}
    for i in f1:
        k=str(i).split("|")
        dict_title[k[0]]=k[1]


    title_final=[]
    for i in range(1,944):
        title1=[]
        for j in range(len(top_recommandation[i])):
            title1.append(top_recommandation[i][j])
        title_final.append(title1)


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
    for key in dict_finalres.keys():
        print key,dict_finalres[key]



    mean_average_precision=0.0
    Average_precision_sum=0
    Average_recall=0.0
    mean_average_recall=0.0
    total_count=0
    for user in range(1,numOfUser):
        if(len(Test_list[user])>1):
            total_count=total_count+1
            count = 0
            sum = 0.0
            num_of_recommanded=0
            item = Result_top_ten[user]
            i=0
            while (i <len(item) and i < num_of_retrieve):
                if (item[i] in Test_list[user]):
                    num_of_recommanded=num_of_recommanded+1
                    count=count+1
                i=i+1
            if(i>0):
                Average_precision_sum = Average_precision_sum + (float(num_of_recommanded)) /i
                Average_recall = Average_recall + float(num_of_recommanded) / len(Test_list[user])

    mean_average_recall=Average_recall/total_count
    mean_average_precision=(Average_precision_sum)/total_count
    print "mean average precision"
    print mean_average_precision
    print "mean average recall"
    print mean_average_recall
    print num_of_retrieve
    print numOfFaeture
    print steps
    print valueofK
    print " probability[u][i]=pow(x,0.33)s"
    return dict_finalres
