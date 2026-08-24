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
# META       "default_warehouse": "6fdb2475-2fd0-4c25-832e-c7080f0448c7",
# META       "known_warehouses": [
# META         {
# META           "id": "6fdb2475-2fd0-4c25-832e-c7080f0448c7",
# META           "type": "Lakewarehouse"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import col, current_timestamp, row_number
from pyspark.sql.window import Window

# 1. Read cleansed silver table
df_silver = spark.read.table("WS_Fabric_Lab.lh_silver.dbo.silver_products")

# 2. Add Surrogate Key and structure for Gold Analytics
window_spec = Window.orderBy("product_id")

df_gold = df_silver.withColumn("product_sk", row_number().over(window_spec)) \
    .select(
        col("product_sk"),
        col("product_id"),
        col("product_name"),
        col("brand"),
        col("category"),
        col("price"),
        col("discount_percentage"),
        col("rating"),
        col("stock_quantity"),
        col("sku"),
        col("weight"),
        current_timestamp().alias("last_updated")
    )

# 3. Save as Delta Parquet table in Gold
df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("WS_Fabric_Lab.lh_gold.dbo.dim_product")

print("Gold dimension table dim_product created successfully!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
