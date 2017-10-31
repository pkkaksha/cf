import numpy as np

# Read the Ratings
def training():
    numOfitem=1683
    numOfUser=944
    Q=np.zeros(shape=(numOfUser,numOfitem))
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
    W = np.zeros(shape=(numOfUser,numOfitem))
    # set user Oreinted Weithing
    for i in range(1,numOfUser):
        count=0
        for j in range(1,numOfitem):
            if(Q[i][j]>0):
                count=count+1
        weight=(float(count)/numOfitem)
        for j in range(1,numOfitem):
            if(Q[i][j]>0):
                W[i][j]=1
            else:
                W[i][j]=weight
    # Definfing Parameters
    lambda_ = 0.05
    n_factors =25
    m, n = Q.shape
    n_iterations =1
    num_of_retrieve=10


    # random initiliase Factor  matrix
    X = np.random.rand(m, n_factors)
    Y = np.random.rand(n_factors, n)


    # calculate error
    def get_error(Q, X, Y, W):
        return np.sum((W * (Q - np.dot(X, Y)))**2)

    errors = []
    for ii in range(n_iterations):
        X = np.linalg.solve(np.dot(Y, Y.T) + lambda_ * np.eye(n_factors), 
                            np.dot(Y, Q.T)).T
        Y = np.linalg.solve(np.dot(X.T, X) + lambda_ * np.eye(n_factors),
                            np.dot(X.T, Q))
        if ii % 100 == 0:
            print('{}th iteration is completed'.format(ii))
        errors.append(get_error(Q, X, Y, W))
    Q_hat = np.dot(X, Y)

    #print('Error of rated movies: {}'.format(get_error(Q, X, Y, W)))

    top_recommandation=[] #all new recommandations Rating
    for i in range(numOfUser):
        top_recommandation.append([])
        for j in range(numOfitem):
            if((Q[i][j]>0)):
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

    f2 = open('/home/pshall/Desktop/sem_project/ml-100k/u2.test', 'r')

    for line in f2:
        my_list = line.split("\t")
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
    # for key in dict_finalres.keys():
        # print key,dict_finalres[key]




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
    print "fdfdsfsf"            
    mean_average_recall=Average_recall/total_count
    mean_average_precision=(Average_precision_sum)/total_count
    print "mean average precision"
    print mean_average_precision
    print "mean average recall"
    print mean_average_recall
    print n_iterations
    print n_factors        
    return dict_finalres
    
