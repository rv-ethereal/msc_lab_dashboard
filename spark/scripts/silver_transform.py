from pyspark.sql import SparkSession
from delta.tables import DeltaTable

spark = SparkSession.builder.appName("silver_transform").getOrCreate()

bronze_path = "s3a://minio-bucket/bronze/sample_delta"
silver_path = "s3a://minio-bucket/silver/sample_delta"

df = spark.read.format("delta").load(bronze_path)

# example cleaning
df2 = df.dropna(subset=["id"]).withColumnRenamed("amount", "amount_raw")
df2 = df2.withColumn("amount", df2["amount_raw"].cast("double"))

df2.write.format("delta").mode("overwrite").save(silver_path)
spark.stop()
