import re
def traindata():
	numOfUser=6041
	numOfitems=3953
	R=[]
	time=[]
	for i in range(0,6041):
	    R.append([])
	def readData():
	    f = open('/home/pshall/Desktop/sem_project/ml-100k/ratings.dat', 'r')
	    for line in f:
		my_list = line.split("::")
		R[int(my_list[0])].append((int(my_list[1]),int(my_list[2]),int(my_list[3])))


	def generate(Ratings):
	    Train = open("/home/pshall/Desktop/sem_project/train_80.txt", 'w')
	    Test=open("/home/pshall/Desktop/sem_project/test_80.txt", 'w')
	    for i in range(1,6041):
		lenght=len(Ratings[i])
		t=int((lenght)*(0.8))
		for j in range(t+1):
		    Train.write(str(i))
		    Train.write("::")
		    Train.write(str(Ratings[i][j][0]))
		    Train.write("::")
		    Train.write(str(Ratings[i][j][1]))
		    Train.write("::")
		    Train.write(str(Ratings[i][j][2]))
		    Train.write("\n")
		for j in range(t+1,int(lenght)):
		    Test.write(str(i))
		    Test.write("::")
		    Test.write(str(Ratings[i][j][0]))
		    Test.write("::")
		    Test.write(str(Ratings[i][j][1]))
		    Test.write("::")
		    Test.write(str(Ratings[i][j][2]))
		    Test.write("\n")




	def timing():
	    for i in range(numOfitems):
		time.append([])
	    f = open('/home/pshall/Desktop/sem_project/ml-100k/movies.dat', 'r')
	    t = open("/home/pshall/Desktop/sem_project/time1.txt", 'w')
	    for line in f:
		my_list = line.split("::")
		#R[int(my_list[0])].append((int(my_list[1]), int(my_list[3])))
		string=my_list[1]
		allt=re.findall('\d+', string)
		j=0
		while(int(allt[j])<1900):
		    j=j+1
		t.write(str(my_list[0]))
		t.write("::")
		t.write(str(allt[j]))
		t.write("\n")


	readData()

	for i in range(1,6041):
	    R[i] = sorted(R[i], key=lambda top_recommandation: top_recommandation[2],
		                           reverse=False)
	generate(R)

	timing()


