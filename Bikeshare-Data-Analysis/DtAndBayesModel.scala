package project

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.mllib.classification.NaiveBayes
import org.apache.spark.mllib.tree.DecisionTree
import org.apache.spark.rdd.RDD
import org.apache.spark.mllib.classification.NaiveBayes
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.tree.DecisionTree


object charuData1 {
	def main(args: Array[String]) = {

			val conf = new SparkConf()
					.setAppName("q3")
					.setMaster("local")

					val sc = new SparkContext(conf)
					sc.setLogLevel("error")

					val weatherData = sc.textFile("dataset/new_weather_data_ml.csv").mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter }

			//  weatherData.take(5).foreach(println)

			val temp = weatherData.map { line => line.split(",")}.filter { x => ! x(4).isEmpty() }

			val tempCat = temp.map(x => List(x(1).toInt, (x(2).toInt/10).toInt,(x(3).toInt/10).toInt,eventcat(x(9)), labelCat(x(10))))


					val parsedData = tempCat.map(v => LabeledPoint(v(4).toInt, Vectors.dense(v(0).toInt, v(1).toInt,v(2).toInt,v(3).toInt)))

					/*
					Predict a custom data point. 
					val test1 = LabeledPoint(22, Vectors.dense(95113,76,61,0))
					val rdd = sc.parallelize(Seq(test1))
					 */

					tempCat.take(5).foreach(println)

					val splits = parsedData.randomSplit(Array(0.90, 0.10))
					val training = splits(0)
					val test = splits(1)
					// val test = rdd
					val numClasses = 45
					val categoricalFeaturesInfo = Map[Int, Int]()
					val impurity = "gini"
					val maxDepth = 5
					val maxBins = 30
					val decisionTreeModel = DecisionTree.trainClassifier(training, numClasses, categoricalFeaturesInfo, impurity, maxDepth, maxBins)
					val predictionAndLabelDT = test.map(p => (decisionTreeModel.predict(p.features), p.label))
					//	predictionAndLabelDT.foreach(println)
					val decisionTreeAccuracy = (1.0 * predictionAndLabelDT.filter(x => x._1 == x._2).count() / test.count())*100
					val naiveBayesModel = NaiveBayes.train(training, lambda= 0.5, modelType = "multinomial")
					val predictionAndLabelNB = test.map(p => (naiveBayesModel.predict(p.features), p.label))
					val naiveBayesAccuracy = (1.0 * predictionAndLabelNB.filter(x => x._1 == x._2).count() / test.count())*100
					//predictionAndLabelNB.foreach(println)

					println("Decision Treee Accuracy is: "+decisionTreeAccuracy + " %" )
					println("Naive Bayes Accuracy is: "+naiveBayesAccuracy + " %" )          
	}

	def labelCat(v: String): Int = {
			if(v == ""){
				return 0
			}
			else{	
				return (v.toInt/100).toInt
			}

	}



	def eventcat(et: String): Int = {
			if(et ==  "Fog" || et == "Fog-Rain"){
				return 1
			}
			else if (et == "Rain" || et == "Rain-Thunderstorm") {
				return 2
			}
			else{
				return 0
			}

	}

	def humiditycat(v: String): Int = {
			if(v == ""){
				return 0
			}
			else{	
				return (v.toInt/10).toInt
			}

	}

}