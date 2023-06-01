def is_allowed(item, whitelist=[]):
    return item in whitelist


def is_list_allowed(checklist, whitelist):
    return all(x in whitelist for x in checklist)
