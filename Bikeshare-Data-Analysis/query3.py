from datetime import datetime
from pyspark.sql.functions import col, udf
from pyspark.sql.types import DateType

def getZip(st):
	if st == 'Mountain View':
		return 94041
	elif st == 'Palo Alto':
		return 94301
	elif st == 'Redwood City':
		return 94063
	elif st == 'San Jose':
		return 95113
	elif st == 'San Francisco':
		return 94107


StationData  = sc.textFile('/Users/charuarora/Downloads/babs_open_data_year_1/201402_babs_open_data/201402_station_data.csv').map(lambda x: x.split(','))

S_Header = StationData.first()

s_data = StationData.filter(lambda row: row !=S_Header).map(lambda x: (x[0], getZip(x[5])))


StatusData  = sc.textFile('/Users/charuarora/Downloads/babs_open_data_year_1/201402_babs_open_data/201402_status_data.csv').map(lambda x: x.split(','))

St_Header = StatusData.first()

st_data = StatusData.filter(lambda row: row !=St_Header).map(lambda x: ((x[0][1:-1],x[3][1:-1].split(' ')[0]), int(x[2][1:-1])))


AveragedStatusData = st_data.groupByKey().mapValues(lambda x: sum(x)/len(x));

CombinedData = AveragedStatusData.map(lambda x:(x[0][0],(x[0][1],x[1]))).join(s_data)

Result = CombinedData.map(lambda x: ( (datetime.strptime(x[1][0][0],'%Y/%m/%d').isoformat().split("T")[0],x[1][1]),x[1][0][1])).reduceByKey(lambda a, b: a + b)

WeatherData  = sc.textFile('/Users/charuarora/Downloads/babs_open_data_year_1/201402_babs_open_data/201402_weather_data.csv').map(lambda x: x.split(','))

w_Header = WeatherData.first()

w_data = WeatherData.filter(lambda row: row !=w_Header)

IndexedWeatherData = w_data.map(lambda x: ((datetime.strptime(x[0], '%m/%d/%Y').isoformat().split("T")[0],int(x[23])),(x[2],x[5],x[8],x[11],x[14],x[17],x[19],x[21])))

NewResult = Result.join(IndexedWeatherData)


Final = NewResult.map(lambda x: (x[0][0],x[0][1],x[1][1][0] ,x[1][1][1],x[1][1][2],x[1][1][3],x[1][1][4],x[1][1][5],x[1][1][6],x[1][1][7] ,x[1][0]))


df = sqlContext.createDataFrame(Final, ['date','zipcode','temp', 'dewpoint','humidity','sealevel','visibility','windspeed','precipitation','event','count'])
df.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").save("/Users/charuarora/Documents/UTD/Spring_2017/BigData/project/weather/weather2014.csv")

