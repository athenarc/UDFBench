

CREATE OR REPLACE FUNCTION extractday_sql(input_date STRING)
RETURNS INT
BEGIN
    RETURN IFTHENELSE(
        trim(input_date,'0123456789-') = '',
        NULLIF(split_part(input_date, '-', 3),''),                
        NULL                                                          
    );
END;