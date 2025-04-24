def extractfunder(project):
     if project:
        try:
            if '::' in project:
                return project.split("::")[0]
            else:
                return None
        except:
            return None
     else:
        return None

extractfunder.registered = True