def cleandate(pubdate):
    if pubdate:
        try:
            if "-" in pubdate:
                splitnum = pubdate.count('-')
                pubdate_split = pubdate.split("-")
                if splitnum ==1:
                    return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                elif splitnum ==2:
                    return pubdate_split[0] + "/" + pubdate_split[1] + "/" + pubdate_split[2]
                else:
                    return None
            elif "/" in pubdate:
                splitnum = pubdate.count('/')
                pubdate_split = pubdate.split("/")
                if splitnum ==1:
                    return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                elif splitnum ==2:
                    return pubdate_split[0] + "-" + pubdate_split[1] + "-" + pubdate_split[2]
                else:
                    return None
            else:
                return None
        except:
            return None
    else:
        return None
cleandate.registered = True