# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "c5c2932d-cce2-4e1c-9904-bc4b7215b54a",
# META       "default_lakehouse_name": "lh_silver",
# META       "default_lakehouse_workspace_id": "f16ab152-d476-4d68-9ca9-80c3d2d310b5",
# META       "known_lakehouses": [
# META         {
# META           "id": "c5c2932d-cce2-4e1c-9904-bc4b7215b54a"
# META         }
# META       ]
# META     },
# META     "warehouse": {
# META       "default_warehouse": "81c5fded-c3a8-4a80-955d-48d0d8e3d1ba",
# META       "known_warehouses": [
# META         {
# META           "id": "81c5fded-c3a8-4a80-955d-48d0d8e3d1ba",
# META           "type": "Lakewarehouse"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import col, current_timestamp, trim, lower

# 1. Read raw table from bronze lakehouse
df_bronze = spark.read.table("WS_Fabric_Lab.lh_bronze.dbo.raw_products")

# 2. Select, rename, clean, and cast appropriate data types
df_silver = df_bronze.select(
    col("`products.id`").cast("integer").alias("product_id"),
    trim(col("`products.title`")).alias("product_name"),
    lower(trim(col("`products.category`"))).alias("category"),
    col("`products.price`").cast("double").alias("price"),
    col("`products.discountPercentage`").cast("double").alias("discount_percentage"),
    col("`products.rating`").cast("double").alias("rating"),
    col("`products.stock`").cast("integer").alias("stock_quantity"),
    trim(col("`products.brand`")).alias("brand"),
    col("`products.sku`").alias("sku"),
    col("`products.weight`").cast("double").alias("weight")
) \
.dropDuplicates(["product_id"]) \
.withColumn("ingestion_timestamp", current_timestamp())

# 3. Write clean data into silver_lakehouse as a Delta table
df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("WS_Fabric_Lab.lh_silver.dbo.silver_products")

print("Silver transformation completed successfully!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
