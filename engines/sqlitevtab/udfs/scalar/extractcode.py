def extractcode(project):
    if project:
        try:
            return project.split("::")[2]
        except:
            return None
    else:
        return None
extractcode.registered = True