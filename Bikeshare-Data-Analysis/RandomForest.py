from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors

RDD1 = sc.textFile("data.csv")
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

# considering only zipcode,temp,humidity,windspeed,(precipitation-nope),event,count

RDD3 = RDD2.map(lambda x: [int(x[1]), int(int(x[2])/10), humiditycat(x[4]),eventcat(x[9]),int(int(x[10])/80)])

def parseLine(x):
	for i in x:
		float(i)
	return LabeledPoint(x[4],Vectors.dense(x[:4]))

data = RDD3.map(lambda x:parseLine(x))

(trainingData, testData) = data.randomSplit([0.7, 0.3])

#DECISION TREE
numClasses = 9;
categoricalFeaturesInfo = {}
impurity = "gini";
featureSubsetStrategy="auto"
maxDepth = 6;
maxBins = 100;
numTrees = 3

model = RandomForest.trainClassifier(trainingData, numClasses, categoricalFeaturesInfo,numTrees, featureSubsetStrategy,impurity, maxDepth, maxBins)

predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testAccuracy = (labelsAndPredictions.filter(lambda (v, p): v == p).count() / float(testData.count()))*100

print "Accuracy of RandomForest:",testAccuracy

#new Test Data
zipcode = 94107
temp = 75
humidity = 51
event = 1
testPoint = [zipcode,temp,humidity,event]

predictedAccuracy = model.predict(testPoint)*100

print "Prediction for Test data:", predictedAccuracy
