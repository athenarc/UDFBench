#include "postgres.h"
#include "fmgr.h"
#include "utils/builtins.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

PG_MODULE_MAGIC;

PG_FUNCTION_INFO_V1(extractmonth_c);
Datum extractmonth_c(PG_FUNCTION_ARGS)
{

	char *mystr = TextDatumGetCString(PG_GETARG_DATUM(0));
	char *end_ptr;
	long val;
	int32 start = -1;
	int32 end = -1;
	int32 year = -1;
	int32 count = 0;
	for (int i = 0; i < strlen(mystr); i++)
	{
	
		if (mystr[i] == '-'){
			if (count==0){
				start = i;
				count++;
			}
			else{
				end = i;
				break;
			}

		}
	
	}
	if ((end > start) && (end > 0) && (start >= 0))
	{
		char *sub_str = (char *)palloc(end - start);
		strncpy(sub_str, mystr + start + 1, end - start - 1);
		sub_str[end - start - 1] = '\0';
		val = strtol(sub_str, &end_ptr, 10);
		pfree(sub_str);
		if (val != (int)val || val == 0)
			PG_RETURN_INT32(year);
		else
			PG_RETURN_INT32((int32)val);
	}
	else
		PG_RETURN_INT32(year);

}