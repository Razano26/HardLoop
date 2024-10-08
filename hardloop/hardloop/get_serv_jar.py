import re
import sys

import requests

baseUrl = "piston-meta.mojang.com"


def get_url_for_version(version_id, data):
    for v in data["versions"]:
        if v["id"] == version_id:
            print("URL: ", v["url"])
            return v["url"]
    print("Version not found")
    sys.exit(1)


def get_server_jar_url(version_url):
    version_data = requests.get(version_url).json()
    print("Server jar url: ", version_data["downloads"]["server"]["url"])
    return version_data["downloads"]["server"]["url"]


def download_server_file(mc_version=None):
    allVersions = None

    # Get the minecraft server version wanted
    if mc_version is not None:
        # Ceck if the version has valid format with regex
        if re.match(r"^([0-9]+)\.([0-9]+)\.([0-9])", mc_version):
            print("Version: ", mc_version)
        else:
            print("Invalid version format, expected x.x.x")
            sys.exit(1)
    else:
        print("No version provided getting the latest version")
        # If no version is provided, get the latest version
        allVersions = requests.get(
            f"https://{baseUrl}/mc/game/version_manifest.json"
        ).json()

        mc_version = allVersions["latest"]["release"]
        print("Version: ", mc_version)

    # Get the url to the selected version

    if allVersions is None:
        allVersions = requests.get(
            f"https://{baseUrl}/mc/game/version_manifest.json"
        ).json()

    versionUrl = get_url_for_version(mc_version, allVersions)
    serverJarUrl = get_server_jar_url(versionUrl)

    # Download the server jar
    serverJar = requests.get(serverJarUrl)
    with open("server.jar", "wb") as f:
        f.write(serverJar.content)
        print("Server jar downloaded")
