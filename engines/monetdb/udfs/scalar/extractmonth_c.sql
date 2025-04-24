


CREATE OR REPLACE FUNCTION extractmonth_c(input STRING)
RETURNS INT
LANGUAGE C {
    #include <string.h>
    size_t i, j;
    result->initialize(result, input.count);
    for(i = 0; i < input.count; i++) {
        if (input.is_null(input.data[i])) {
            // handle NULL values
            result->data[i] = result->null_value;
        } else  {
            // reverse the input string
            char* input_string = input.data[i];
            size_t len = strlen(input_string);
            int start = -1;
            int end = -1;
            int month = result->null_value; 
            int count = 0;
            for (int i = 0; i < len; i++)
            {
                
                if (input_string[i] == '-'){
                    if (count==0){
                        start = i;
                        count++;

                    }
                    else {
                        end = i;
                        break;

                    }
                }
               
                
            }
            if ((end > start) && (end > 0) && (start >= 0)  && (end - start > 2))
                {
                    char sub_str[3];
                    strncpy(sub_str, input_string + start + 1, end - start - 1);
                    sub_str[end - start ] = '\0';
                    long val;
                    char *end_ptr;
                    val = strtol(sub_str, &end_ptr, 10);

                    if (val != (int)val || val == 0)
                       result->data[i]=month;
                    else
                        result->data[i]=(int)val;
                }
                else
                    result->data[i]=month;
          
        }
    }
};
