from pyspark.mllib.tree import GradientBoostedTrees, GradientBoostedTreesModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors

RDD1 = sc.textFile("/Users/Josina/Documents/sem4/Big data/Project/ML/data.csv")
RDD2 = RDD1.map(lambda x: x.split(',')).filter(lambda x: x[4] != '' )

def eventcat(et):
	if (et ==  'Fog'):
		return 1 
	elif (et =='Fog-Rain'):
		return 2
	elif (et == 'Rain'):
		return 3
	elif (et == 'Rain-Thunderstorm'):
		return 4
	else:
		return 0

def humiditycat(v):
	if v == '':
		return 0
	else:
		return int(int(v)/20) 

# considering only zipcode,temp,humidity,,event,count

#RDD3 = RDD2.map(lambda x: [int(x[3]), int(int(x[4])/10), humiditycat(x[6]),int(int(x[9])/5),eventcat(x[11]),int(int(x[12])/100)])

RDD3 = RDD2.map(lambda x: [int(x[1]), int(int(x[2])/10), humiditycat(x[3]),eventcat(x[9]),int(int(x[10])/100)])

def parseLine(x):
	for i in x:
		float(i)
	return LabeledPoint(x[4],Vectors.dense(x[:4]))

data = RDD3.map(lambda x:parseLine(x))

(trainingData, testData) = data.randomSplit([0.6, 0.4])

#GRADIENT BOOST
model = GradientBoostedTrees.trainClassifier(trainingData, categoricalFeaturesInfo={}, numIterations=8)

predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testAccuracy = (labelsAndPredictions.filter(lambda (v, p): v == p).count() / float(testData.count()))*100

print "Accuracy of Gradient Boosting:",testAccuracy

#new Test Data
zipcode = 95113
temp = 76
humidity = 61
event = 0
testPoint = [zipcode,temp,humidity,event]

predictedAccuracy = model.predict(testPoint)*100

print "Prediction for Test data:", predictedAccuracy
