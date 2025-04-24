
def extractid(project):
     if project:
        try:
            return project.split("::")[2]
        except:
            return None
     else:
        return None

extractid.registered = True