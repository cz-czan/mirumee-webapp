import mirumee_webapp.fetch_spacex.fetch as f
import sys
import getopt

debug = False

limit = 0
include_upcoming = False
include_failed = False


def get_full_core_information(count: int = 0, _include_upcoming: bool = False, _include_failed: bool = False):
    """
        Crosses/links information fetched by fetch.fetch_cores_information() and fetch.fetch_missions_information() so
        that we get a list containing tuples with:
            - a core's id
            - it's reuse count
            - the total mass of the payloads it carried to space in all missions it took part in ( in the first stage ).
        in the following format:
            (<core id>, <core reuse count>, <core's total payload mass delivered to space throughout all missions>)
    """
    complete_core_information = []
    missions_information = f.fetch_missions_information(_include_upcoming)

    # Assuming that an upcoming mission can't fail since it hasn't started

    cores_information = f.fetch_cores_information(count)["data"]["cores"]

    for core in cores_information:
        # List of lists containing the mission names and
        total_payload_mass = 0

        for mission in missions_information:
            try:
                # IDs of all cores in the first stage of the rocket used in this mission.
                mission_fs_core_ids = [core["core"]["id"] for core in mission["rocket"]["first_stage"]["cores"]]
            except TypeError:
                # A type error will be raised only if there are no cores in a first stage of a mission, e.g. for an upcoming
                # mission, because naturally the returned None object is not subscriptable
                continue

            # List comprehension and a "short if" is used below to avoid using unnecessary loops and long if statements.
            mission_total_payload_mass = sum(
                [payload["payload_mass_kg"] if type(payload["payload_mass_kg"]) == int else 0 for payload in
                 mission["rocket"]["second_stage"]["payloads"]])

            for fs_core_id in mission_fs_core_ids:
                if core['id'] in mission_fs_core_ids:
                    if not _include_failed:
                        if not mission["launch_success"]:
                            missions_information.remove(mission)

                            # Reuses in failed missions are counted by the API in the response to the core query
                            # that's why we have to subtract them ourselves
                            if core['reuse_count'] > 0:
                                core['reuse_count'] -= 1
                            break

                    # Reuses in upcoming missions are not counted by the API in the response to the core query that's
                    # why we have to add them ourselves
                    if mission["upcoming"] and include_upcoming:
                        if debug:
                            core['reuse_count'] += 1
                            print(f"{core['id']} will take part in mission {mission['mission_name']}"
                                  f" and deliver a payload of {mission_total_payload_mass} kg")
                    else:
                        if debug:
                            print(f"{core['id']} took part in mission {mission['mission_name']}"
                                  f" and delivered a payload of {mission_total_payload_mass} kg")

                    total_payload_mass += mission_total_payload_mass
                    break
        if debug:
            print(
                f"{core['id']}'s total payload mass delivered throughout all missions "
                f"{'(including upcoming missions)' if _include_upcoming  else ''}  is: {total_payload_mass} kgs.\n"
                f"It {'had/will have' if _include_upcoming  else 'had'} been reused {core['reuse_count']} times.\n")

        complete_core_information.append((core['id'], core['reuse_count'], total_payload_mass))

    return complete_core_information


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:ufd", ["limit", "upcoming", "failed", "debug"])

        for o, v in opts:
            if o in ("-l", "--limit"):
                limit = v
            if o in ("-u", "--upcoming"):
                include_upcoming = True
            if o in ("-f", "--failed"):
                include_failed = True
            if o in ("-d", "--debug"):
                debug = True

    except getopt.GetoptError as err:
        print(str(err))

    print(get_full_core_information(limit if limit != 0 else 0, include_upcoming, include_failed))
