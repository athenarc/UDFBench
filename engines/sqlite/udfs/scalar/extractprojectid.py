import re
def extractprojectid(input):
    if input:
        try:
            return re.findall(r"(?<!\d)[0-9]{6}(?!\d)",input)[0]
        except:
            return ''
    else:
        return None

extractprojectid.registered = True