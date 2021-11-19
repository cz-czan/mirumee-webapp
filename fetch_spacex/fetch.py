import requests
import os.path

url = "http://api.spacex.land/graphql"
headers = {
    'Content-Type': 'application/json'
}

# The queries are stored in .txt files to avoid clutter in the source
with open(os.path.dirname(__file__) + '/queries/past_missions.txt', 'r') as fs:
    missions_query = fs.read()
with open(os.path.dirname(__file__) + '/queries/cores.txt', 'r') as fs:
    cores_query = fs.read()


def fetch_missions_information(upcoming: bool = False):
    """
            Fetches the following information about all the missions/launches from the API:
                - the mission names
                - the ids of cores within the first stage of the rocket launched in the mission
                - the payload mass carried to space, in kgs.
    """

    missions_information = \
        requests.request("POST", url, headers=headers, data=missions_query).json()["data"]["launchesPast"]

    for mission in missions_information:
        mission["upcoming"] = False

    if upcoming:
        upcoming_query = missions_query.replace('launchesPast', 'launchesUpcoming')
        upcoming_missions_info = \
            requests.request("POST", url, headers=headers, data=upcoming_query).json()["data"]["launchesUpcoming"]

        for mission in upcoming_missions_info:
            mission["upcoming"] = True

        missions_information += upcoming_missions_info

    # the "filter:" option for launches in the GraphQL API can only filter by string values, and not booleans, therefore
    # the removal of missions with failed flights has to be done after receiving the data, and not in the query (the
    # launch_success field is a boolean type field).

    return missions_information


def fetch_cores_information(count: int = 0):
    """
        Fetches the following information about all the cores from the API:
            - the core's id
            - the names of missions where the core was used
            - the reuse count
    """

    _cores_query = cores_query.replace(', limit: 10', f', limit: {count}' if count > 0 else '')
    return requests.request("POST", url, headers=headers, data=_cores_query).json()
