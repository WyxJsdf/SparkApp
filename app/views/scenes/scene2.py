# -*- coding: utf-8 -*-
from __future__ import print_function

from pyspark.sql import SparkSession
from datetime import datetime
import sys


def transform1(line):
  RentalStart = line[12]
  Price = line[5]
  Currency = line[7]
  rtime = datetime(2011, 11, 1, 0, 0)
  rprice = 0.0
  rcurrency = 1.0
  if RentalStart != "RentalStart":
    mtime = RentalStart.split(".")[0]
    rtime = datetime.strptime(mtime, "%Y-%m-%d %H:%M:%S")
  if Price != "Price":
    rprice = float(Price)
  if Currency != "Currency" and Currency == "US":
    rcurrency = 6.8933
  return (rtime, rprice, rcurrency)


def date2day(date):
  if isinstance(date, datetime):
    return datetime(date.year, date.month, date.day)


def date2quarter(date):
  if isinstance(date, datetime):
    return datetime(date.year, 1+3*(int((date.month-1) / 3 + 1) - 1), 1)


def date2year(date):
  if isinstance(date, datetime):
    return datetime(date.year, 1, 1)


def statsitic_for_currency(lines):
  rdd1 = lines.map(lambda x: (x.split(',')[7], 1)).reduceByKey(lambda a, b: a+b)
  output = rdd1.collect()
  for k, v in output:
    print("%s: %d" % (k, v))


def statsitic_for_rentstart(lines):
  rdd1 = lines.map(lambda x: transform1(x.split(','))[0])
  min_output = rdd1.min()
  max_output = rdd1.max()
  print("min date: %s\nmax date: %s" % (min_output, max_output))


def statistic_scene2(lines):
  rdd1 = lines.map(lambda x: transform1(x.split(',')))
  
  rdd2 = rdd1.map(lambda x: (date2day(x[0]), [x[1]*x[2], x[1]>0]))
  day_level = rdd2.reduceByKey(lambda a, b: [a[0]+b[0], a[1]+b[1]]).sortByKey()
  day_output = day_level.collect()
  
  rdd3 = rdd1.map(lambda x: (date2quarter(x[0]), [x[1]*x[2], x[1]>0]))
  quarter_level = rdd3.reduceByKey(lambda a, b: [a[0]+b[0], a[1]+b[1]]).sortByKey()
  quarter_output = quarter_level.collect()
  
  rdd4 = rdd1.map(lambda x: (date2year(x[0]), [x[1]*x[2], x[1]>0]))
  year_level = rdd4.reduceByKey(lambda a, b: [a[0]+b[0], a[1]+b[1]]).sortByKey()
  year_output = year_level.collect()
  
  # data like [{datetime, [total, number]}]
  return day_output, quarter_output, year_output


def scene2(lines, start_time, end_time):
  rdd1 = lines.map(lambda x: transform1(x.split(',')))
  rdd2 = rdd1.filter(lambda x: x[0] >= start_time and x[0] <= end_time)
  rdd_buy = rdd2.map(lambda x: (x[1] > 0, 1))
  rdd_buy_num = rdd_buy.reduceByKey(lambda a, b: a+b)
  num_output = rdd_buy_num.collect()
  num = 0
  print_info = ''
  for k, v in num_output:
    if k == 1:
      print_info = "From %s to %s, there were %d times TVPrograms-buying." % (start_time, end_time, v)
      num = v
  if num == 0:
    print("From %s to %s, there were 0 times TVPrograms-buying")
  else:
    rdd_price = rdd2.map(lambda x: (x[1] > 0, x[1]*x[2]))
    rdd_price_avg = rdd_price.reduceByKey(lambda a, b: a+b)
    avg_output = rdd_price_avg.collect()
    for k, v in avg_output:
      if k == 1:
        avg = v / num
        print("%s\nAverage price is %f" % (print_info, avg))


def get_lines():
  spark = SparkSession.builder.appName("Scene2").getOrCreate()
  filename = "hdfs://Master:9000/data/Purchase.csv"
  lines = spark.read.text(filename).rdd.map(lambda r: r[0])
  return lines


def stop():
  spark.stop()

# if __name__ == "__main__":
#   '''
#   if len(sys.argv) != 3:
#     print("""Usage: scene2.py "%Y-%m-%d %H:%M:%S" "%Y-%m-%d %H:%M:%S" """)
#     print("Such as scene2.py \"2011-10-1 0:0:0\" \"2011-12-30 23:59:0\"")
#     exit(-1)
#   '''
#   spark = SparkSession.builder.appName("Scene2").getOrCreate()
#   filename = "hdfs://Master:9000/data/Purchase.csv"
#   '''
#   try:
#     start_time = datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M:%S")
#     end_time = datetime.strptime(sys.argv[2], "%Y-%m-%d %H:%M:%S")
#     if start_time > end_time:
#       temp = start_time
#       start_time = end_time
#       end_time = temp
#   except:
#     start_time = datetime(2011, 10, 1, 0, 0)
#     end_time = datetime(2011, 12, 30, 23, 59)
#   '''
#   lines = spark.read.text(filename).rdd.map(lambda r: r[0])
#   # statsitic_for_currency(lines)
#   # statsitic_for_rentstart(lines)
#   statistic_scene2(lines)
#   # scene2(lines, start_time, end_time)
#   spark.stop()