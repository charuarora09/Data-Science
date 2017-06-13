StationData  = sc.textFile('/Users/charuarora/Downloads/babs_open_data_year_1/201402_babs_open_data/201402_station_data.csv').map(lambda x: x.split(','))

S_Header = StationData.first()

s_data = StationData.filter(lambda row: row !=S_Header).map(lambda x: (x[0], (x[1],int(x[4]))))


StatusData  = sc.textFile('/Users/charuarora/Downloads/babs_open_data_year_1/201402_babs_open_data/201402_status_data.csv').map(lambda x: x.split(','))

St_Header = StatusData.first()

st_data = StatusData.filter(lambda row: row !=St_Header).map(lambda x: (x[0][1:-1],int(x[2][1:-1])))

status_report  = st_data.groupByKey().mapValues(lambda x: sum(x)/len(x));

report = status_report.map(lambda x: (x[0],x[1]))

final = status_report.join(s_data).map(lambda x:(x[0],x[1][1][0],int(x[1][1][1]),x[1][0],x[1][0]/float(x[1][1][1])*100))


df = sqlContext.createDataFrame(final, ['stationid','name','available docks', 'average used docks', 'percentage of used docks'])
df.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").save("/Users/charuarora/Documents/UTD/Spring_2017/BigData/project/docks_used_2014_1.csv")

