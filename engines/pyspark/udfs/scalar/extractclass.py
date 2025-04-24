# U5.	Extractclass: extracts class from string with format funder::class::projectid 
def extractclass(project:str)->str:
    if project:
        try:
            return project.split("::")[1]
        except:
            return None
    else:
        return None


