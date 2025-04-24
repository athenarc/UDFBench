
def extractclass(project):
    if project:
        try:
            return project.split("::")[1]
        except:
            return None
    else:
        return None

extractclass.registered = True