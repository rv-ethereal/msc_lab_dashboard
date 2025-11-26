from pyspark.sql import SparkSession
import sys
import os

spark = SparkSession.builder \
    .appName("bronze_load") \
    .getOrCreate()

# sample local CSV folder or API pull; here we load data/sample.csv
input_path = "/data/sample.csv"
bronze_path = "s3a://minio-bucket/bronze/sample_delta"

df = spark.read.option("header", True).csv(input_path)

# write as delta to MinIO S3 endpoint (configure s3a in Spark conf)
df.write.format("delta").mode("append").save(bronze_path)

spark.stop()
