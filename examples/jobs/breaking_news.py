from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

from pyspark.sql.functions import col, split, lit, array_except, length, size, array, explode, count, array_remove
from pyspark.sql.types import *

if __name__ == "__main__":
	app_name = 'DataEngineering'

	conf = SparkConf()

	hdfs_host = 'hdfs://namenode:8020'

	conf.set("hive.metastore.uris", "http://hive-metastore:9083")
	conf.set("spark.kerberos.access.hadoopFileSystem", hdfs_host)
	conf.set("spark.sql.warehouse.dir", f"{hdfs_host}/user/hive/warehouse")
	conf.set("hive.metastore.warehouse.dir", f"{hdfs_host}/user/hive/warehouse")
	conf.setMaster("local[*]") 

	spark = SparkSession \
	      .builder \
	      .appName(app_name) \
	      .config(conf=conf) \
	      .enableHiveSupport()\
	      .getOrCreate()


	schema = StructType([ \
	        StructField("ArticleID",IntegerType(),True), \
	        StructField("Text",StringType(),True), \
	        StructField("Category",StringType(),True)
	      ])

	news = spark.read.option('inferSchema', 'false').schema(schema).csv('/airflow/data/bbc_news.csv')
	stopwords = spark.read.option('header', 'true').csv('/airflow/data/stopwords.txt')

	news.show(1, 1)

	exploded = news\
	            .withColumn('Words', split(col('Text'), ' |\.|,|\:|\!|\?'))\
	            .select(news.ArticleID, news.Category, explode(col('Words')).alias('Word'))\
	            .filter(length(col('Word')) > 2)\
	            .where("Word != ''")\


	# exploded.show(5)

	drop_nums = exploded\
	            .withColumn('IsNumber', col('Word').cast('int').isNotNull())\
	            .where(~col('IsNumber'))\
	            .drop('IsNumber')\

	filter_stop_words = drop_nums.alias('w')\
	                      .join(stopwords.alias('s'), col('Word') == col('i'), 'leftanti')

	filter_stop_words.show(10)

	frequencies = filter_stop_words\
	              .groupby('ArticleID', 'Category', 'Word')\
	              .agg(count('*').alias('Freq'))\
	              .where(col('Freq') > 10)

	frequencies.show()



	results = frequencies\
	            .withColumn('rank', row_number()\
	                        .over(
	                                Window.partitionBy('ArticleID', 'Category').orderBy(col('Freq').desc())
	                              ))\
	            .where('rank <= 3')\
	            .withColumnRenamed('Freq', 'Frequency')\
	            .withColumnRenamed('Word', 'Tag')\
	            .select('ArticleID', 'Category', 'Tag', 'Frequency')

	"""Save to various file formats"""

	data_lake_path = f'{hdfs_host}/data_lake'
	data_lake_path

	''' save to CSV '''

	results.write.mode('overwrite').csv(f'{data_lake_path}/frequencies_all.csv')

	''' Save to ORC and partition by Category ''' 

	results \
	  .write \
	  .partitionBy('Category') \
	  .option('orc.compress', 'snappy') \
	  .mode('append') \
	  .orc(f'{data_lake_path}/frequencies_orc')

	spark.read.orc(f'{data_lake_path}/frequencies_orc').show()

	ctlg = spark.catalog

	print(ctlg.listDatabases())

	spark.sql(f"create schema if not exists bbc location '{hdfs_host}/bbc_news_schema'");

	results.write.saveAsTable('bbc.results_as_table', format='parquet', partitionBy=['Category', 'Tag'])

	spark.sql('show databases').show(10, truncate=False)
	spark.sql('show tables in default').show(10, truncate=False)
	spark.sql('describe table extended bbc.results_as_table').show(100, truncate=False)

	spark.sql('select * from bbc.results_as_table').show(100)

	spark.sql('show create table  bbc.results_as_table').show(truncate=False)

	print(spark.table('bbc.results_as_table').count())

	cols = spark.table('bbc.results_as_table').columns 

	results.select(*cols).write.insertInto('bbc.results_as_table', overwrite=False)
	spark.sql('MSCK repair table bbc.results_as_table')

	print(spark.table('bbc.results_as_table').count())

	results.write.option('path', f'{data_lake_path}/bbc_ext_results').saveAsTable('bbc.results_as_external_table', format='parquet')

	spark.sql('describe table extended bbc.results_as_external_table').show(100, truncate=False)

