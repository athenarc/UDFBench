import pyarrow as pa


# U30.	Extractfromdate: Reads a date (as a string) and returns 3 column values (year, month, day)

def _extractfromdate(arg: str):
    try:
        year = int(arg[:arg.find('-')])
        month = int(arg[arg.find('-') + 1:arg.rfind('-')])
        day = int(arg[arg.rfind('-') + 1:])
        return year, month, day
    except:
        return -1, -1, -1


def extractfromdate(batch: pa.Table) -> pa.Table:
    years, months, days = [], [], []

    for v in batch["date"].to_pylist():
        if v is None:
            y, m, d = None, None, None
        else:
            y, m, d = _extractfromdate(v)
        years.append(y)
        months.append(m)
        days.append(d)

    return pa.table({
        "id": batch["id"],
        "year": pa.array(years, pa.int32()),
        "month": pa.array(months, pa.int32()),
        "day": pa.array(days, pa.int32()),
    })


    
