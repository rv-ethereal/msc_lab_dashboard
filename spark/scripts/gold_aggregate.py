from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, sum as _sum

spark = SparkSession.builder.appName("gold_aggregate").getOrCreate()

silver_path = "s3a://minio-bucket/silver/sample_delta"
gold_path = "s3a://minio-bucket/gold/daily_sales_delta"

df = spark.read.format("delta").load(silver_path)

daily = df.groupBy(to_date(df["date"]).alias("day")).agg(_sum("amount").alias("daily_total"))

daily.write.format("delta").mode("overwrite").save(gold_path)
spark.stop()
