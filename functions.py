from mirumee_webapp.fetch_spacex.main import get_full_core_information
from mirumee_webapp.models import RocketCore


def fetch_and_save_rocket_core_data():
    core_data = get_full_core_information()
    for core in core_data:
        core_obj = RocketCore(core_id=core[0], reuse_count=core[1], total_payload_mass=core[2])
        core_obj.save()
