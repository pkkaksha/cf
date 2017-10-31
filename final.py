from flask import Flask,render_template,request
import io
import recomm
from als import *
from timeprob import *
import timeprob
import generate_data
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('1.html')
   
@app.route('/showmovies')
def show():
	listmovie=[]
	#file=open("/home/pshall/Desktop/sem_project/ml-100k/u.item")
	with io.open("/home/pshall/Desktop/sem_project/ml-100k/u.item",encoding = 'utf-8') as f:
  		file=f.readlines()
	for i in file:
		listmovie.append(i.split("|")[1])
		print i.split("|")[1]
	return render_template('2.html',result1=listmovie)

@app.route('/recmethod')
def choose():
	return render_template('3.html')

@app.route('/als')
def als():
	result_dict={}
	result_dict=training()
	return render_template('res.html',result=result_dict)
	#return render_template('4.html')

@app.route('/wals')
def wals():
	result_dict={}
	result_dict=recomm.training()
	return render_template('res.html',result=result_dict,)

@app.route('/timepro')	
def timepro():
	generate_data.traindata()
	result_dict={}
	result_dict=training1()
	return render_template('res.html',result=result_dict)   

# @app.route('/als1',methods=['POST'])
# def alsf1():
# 	testset1=request.form['item1']
# 	print "yes",testset1
# 	#result_list={}
# 	result_list=[]
# 	result_list=xx.training(testset1)
# 	return render_template('res.html',result=result_list)



if __name__ == '__main__':
    app.run(debug = True)
