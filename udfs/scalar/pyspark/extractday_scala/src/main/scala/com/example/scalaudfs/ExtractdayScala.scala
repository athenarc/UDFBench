package com.example.scalaudfs

import org.apache.spark.sql.api.java.UDF1

class ExtractdayScala extends UDF1[String, Integer] {
  override def call(date: String): Integer  = {
    if (date != null && date.contains("-")) {
      try {
        val day = date.split("-")(2).toInt
        return day
      } catch {
        case e: Exception => return -1 
      }
    }
    null 
  }

}
