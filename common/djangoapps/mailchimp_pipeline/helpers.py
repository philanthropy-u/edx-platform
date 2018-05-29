from lms.djangoapps.onboarding.models import (FocusArea, OrgSector, )


def get_org_data_for_mandrill(organization):
    focus_areas = FocusArea.get_map()
    org_sectors = OrgSector.get_map()
    org_label = organization.label if organization else ""

    org_type = ""
    if organization.org_type:
        org_type = org_sectors.get(organization.org_type, "")

    focus_area = str(focus_areas.get(organization.focus_area, "")) if organization else ""

    return org_label, org_type, focus_area
