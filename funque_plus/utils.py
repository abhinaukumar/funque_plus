from videolib import standards

# Should add this to videolib eventually
_standards_dict = {standard.name: standard for standard in standards.supported_standards}
def get_standard(name: str) -> standards.Standard:
    try:
        return _standards_dict[name]
    except KeyError:
        raise KeyError('Invalid standard name')
