import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1714337942592 = glueContext.create_dynamic_frame.from_catalog(database="youtube-db-project-cleansed", table_name="raw_statistics", transformation_ctx="AWSGlueDataCatalog_node1714337942592")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1714337926511 = glueContext.create_dynamic_frame.from_catalog(database="youtube-db-project-cleansed", table_name="cleaned_statistics_reference_data", transformation_ctx="AWSGlueDataCatalog_node1714337926511")

# Script generated for node Join
Join_node1714337968560 = Join.apply(frame1=AWSGlueDataCatalog_node1714337942592, frame2=AWSGlueDataCatalog_node1714337926511, keys1=["category_id"], keys2=["id"], transformation_ctx="Join_node1714337968560")

# Script generated for node Amazon S3
AmazonS3_node1714338087639 = glueContext.getSink(path="s3://youtube-db-project-dataset-analytics", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=["region", "category_id"], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1714338087639")
AmazonS3_node1714338087639.setCatalogInfo(catalogDatabase="youtube_db_analytics",catalogTableName="final_analytics")
AmazonS3_node1714338087639.setFormat("glueparquet", compression="snappy")
AmazonS3_node1714338087639.writeFrame(Join_node1714337968560)
job.commit()