StationInfo  = sc.textFile('/Users/charuarora/Downloads/babs_open_data_year_1/201402_babs_open_data/201402_station_data.csv')
station = StationInfo.map(lambda line: line.split(","))
stationheader = station.first()
station_data = station.filter(lambda row: row !=stationheader).map(lambda x:(x[5],x[1]))

TripInfo  = sc.textFile('/Users/charuarora/Downloads/babs_open_data_year_1/201402_babs_open_data/201402_trip_data.csv')
trip = TripInfo.map(lambda line: line.split(","))
tripheader = trip.first()
trip_data = trip.filter(lambda row: row !=tripheader).map(lambda x:((x[2],x[3]),1)).reduceByKey(lambda a, b: a + b)

tdata = trip_data.map(lambda x: ((x[0][0].split(" ")[0].split("/")[2],x[0][0].split(" ")[0].split("/")[0],x[0][1]),x[1]))
tdata = tdata.keyBy(lambda x:x[0][2])
sdata = station_data.keyBy(lambda x:x[1])
result = tdata.join(sdata).map(lambda x:((x[1][0][0][0],x[1][0][0][1],x[1][1][0]),x[1][0][1]))
r = result.reduceByKey(lambda a, b: a + b).map(lambda x:(x[0][0],x[0][1],x[0][2],x[1]))
df = sqlContext.createDataFrame(r, ['year', 'month','city', 'count'])
df.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").save("/Users/charuarora/Documents/UTD/Spring_2017/BigData/project/result.csv")


tdata = trip_data.map(lambda x: ((x[0][0].split(" ")[0].split("/")[2],x[0][0].split(" ")[0].split("/")[0],x[0][0].split(" ")[0].split("/")[1],x[0][1]),x[1]))
tdata = tdata.keyBy(lambda x:x[0][3])
result = tdata.join(sdata).map(lambda x:((x[1][0][0][0],x[1][0][0][1],x[1][0][0][2],x[1][1][0]),x[1][0][1]))
r = result.reduceByKey(lambda a, b: a + b).map(lambda x:(x[0][0],x[0][1],x[0][2],x[0][3],x[1]))
df = sqlContext.createDataFrame(r, ['year', 'month', 'day','city', 'count'])

data  = sc.textFile('/Users/charuarora/Documents/UTD/Spring_2017/BigData/project/perCityDayMonthYear_count.csv').map(lambda x:x.split(","))
h = data.first()
d = data.filter(lambda row: row !=h).map(lambda x: ((x[0],x[1],x[2],x[3]),x[4]))
x = d.reduceByKey(lambda a, b: a + b).map(lambda x:(x[0][0],x[0][1],x[0][2],x[0][3],x[1]))
df = sqlContext.createDataFrame(x, ['year', 'month','day', 'city', 'count'])
df.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").save("/Users/charuarora/Documents/UTD/Spring_2017/BigData/project/final_result.csv")