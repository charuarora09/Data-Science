TripInfo  = sc.textFile('/Users/charuarora/Downloads/babs_open_data_year_3/201608_trip_data.csv')
trip = TripInfo.map(lambda line: line.split(","))
tripheader = trip.first()
trip_data = trip.filter(lambda row: row !=tripheader).map(lambda x:((x[2],x[10]),1)).reduceByKey(lambda a, b: a + b)
tdata = trip_data.map(lambda x: ((x[0][0].split(" ")[0].split("/")[2],x[0][0].split(" ")[0].split("/")[0],x[0][0].split(" ")[0].split("/")[1],x[0][1]),x[1])).reduceByKey(lambda a, b: a + b)

WInfo  = sc.textFile('/Users/charuarora/Downloads/babs_open_data_year_2/201508_weather_data.csv')
wea = WInfo.map(lambda line: line.split(","))
hea = wea.first()
w_data = wea.filter(lambda row: row !=hea).map(lambda x:((x[0].split("/")[2],x[0].split("/")[0],x[0].split("/")[1],x[23]),(x[2],x[5],x[8],x[11],x[14],x[17],x[19],x[21])))
result = w_data.join(tdata)
r = result.map(lambda x:(x[0][0],x[0][1],x[0][2],x[0][3],x[1][0][0],x[1][0][1],x[1][0][2],x[1][0][3],x[1][0][4],x[1][0][5],x[1][0][6],x[1][0][7],x[1][1]))

df = sqlContext.createDataFrame(r, ['year', 'month', 'day','zipcode','temp', 'dewpoint','humidity','sealevel','visibility','windspeed','precipitation','event','count'])
w.toDF().coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").save("/Users/charuarora/Documents/UTD/Spring_2017/BigData/project/weather.csv")


w = w_data.map(lambda x: [x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17],x[18],x[19],x[20],x[21],x[22],zip(x[23])])

def zip(n):
	if (n ==  '94107'):
		return 'San Francisco' 
	elif (n =='94063'):
		return 'Redwood City'
	elif (n == '94301'):
		return 'Palo Alto'
	elif (n == '94041'):
		return 'Mountain View'
	else:
		return 'San Jose'
		
