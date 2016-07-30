
from pyspark.sql import SQLContext, Row
sqlContext = SQLContext(sc)

# Load a text file and convert each line to a Row.
lines = sc.textFile("/user/cloudera/departments_2/")
parts = lines.map(lambda l: l.split(","))
department = parts.map(lambda p: Row(id=int(p[0]),name=p[1]))

lines = sc.textFile("/user/cloudera/categories/")
parts = lines.map(lambda l: l.split(","))
categories = parts.map(lambda p: Row(seqid=int(p[0]),depid=int(p[1]),prdname=p[2]))

# Infer the schema, and register the DataFrame as a table.
schemadep = sqlContext.createDataFrame(department)
schemadep.registerTempTable("department")

schemacat = sqlContext.createDataFrame(categories)
schemacat.registerTempTable("categories")

# SQL can be run over DataFrames that have been registered as a table.
departmentf = sqlContext.sql("SELECT name FROM department WHERE id >= 1 ")
categoryf = sqlContext.sql("SELECT prdname,depid FROM categories WHERE depid >= 1 ").collect()
categoryf = sqlContext.sql("SELECT sum(depid), prdname as total FROM categories WHERE depid >= 1 group by prdname ")


#joinf =sqlContext.sql("SELECT prdname FROM categories inner join department  WHERE categories.depid = department.id and department.id=5 ")

# The results of SQL queries are RDDs and support all the normal RDD operations.

catenames = categoryf.map(lambda (g,x): "Name: " + g.prdname + x.depid )

for catename in catenames.collect():
   print catename


depnames = departmentf.map(lambda p: "Name: " + p.name)
for teenName in depnames.collect():
  print teenName
