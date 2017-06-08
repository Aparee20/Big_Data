from pyspark import SparkContext
from pyspark import SparkConf
import json
 
sc = SparkContext()
 
manifest = sc.textFile("file")
 
manifest_content = ' '.join(str(x) for x in manifest.collect())
 
file_list_json = json.loads(manifest_content)
 
file_list = ','.join(x['url'] for x in file_list_json['entries'])
 
data_rdd = sc.textFile(file_list).map(lambda x: x.split("|"))
 
for x in data_rdd.collect():
      print x
