package com.example.udfs;

import org.apache.spark.sql.api.java.UDF1;

public class ExtractmonthJava implements UDF1<String, Integer> {
    @Override
    public Integer call(String arg) {
        if (arg != null && !arg.isEmpty()) {
            try {
                int firstDash = arg.indexOf('-');
                int lastDash = arg.lastIndexOf('-');
                
                if (firstDash != -1 && lastDash != -1 && firstDash < lastDash) {
                    String monthStr = arg.substring(firstDash + 1, lastDash);
                    return Integer.parseInt(monthStr);
                } else {
                    return -1; 
                }
            } catch (Exception e) {
                return -1; 
            }
        }
        return null; 
     
    }
}