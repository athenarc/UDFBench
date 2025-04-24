-- U30.	Extractfromdate: Reads a date (as a string) and returns 3 column values (year, month, day)

CREATE TYPE _extractfromdate AS (
    extractyear integer, 
    extractmonth integer,
    extractday integer
);

CREATE or replace FUNCTION extractfromdate(arg text)
    RETURNS _extractfromdate
AS $$
        try:
            return {"extractyear":int(arg[:arg.find('-')]),
                    "extractmonth":int(arg[arg.find('-')+1:arg.rfind('-')]),
                    "extractday":int(arg[arg.rfind('-')+1:])
            }
        except:
            return {"extractyear":-1,
                    "extractmonth":-1,
                    "extractday":-1
            }

$$
LANGUAGE 'plpython3u'IMMUTABLE STRICT PARALLEL SAFE;