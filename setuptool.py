import subprocess
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List
import sys
import os

CONFIGS_DIRECTORY = "/configs"
GREEN = '\033[92m'
RESET = '\033[0m'

@dataclass
class Metadata:
    owner: str
    group: str
    mode: str

@dataclass
class DirectoryMove:
    source: str
    destination: str

@dataclass
class Config:
    name: str
    description: str
    version: str
    metadata: Metadata
    services: List[str]
    packages: List[str]
    directoriesToMove: List[DirectoryMove]


def load_config(path: Path) -> Config:
    raw = json.loads(path.read_text(encoding="utf-8"))

    md = raw.get("metadata", {})
    metadata = Metadata(
        owner=md.get("owner", ""),
        group=md.get("group", ""),
        mode=md.get("mode", ""),
    )

    directories = []
    for directory in raw.get("directoriesToMove", []):
        directories.append(DirectoryMove(source=directory.get("source", ""), destination=directory.get("destination", "")))

    return Config(
        name=raw.get("name", ""),
        description=raw.get("description", ""),
        version=raw.get("version", ""),
        metadata=metadata,
        services=list(raw.get("services", [])),
        packages=list(raw.get("packages", [])),
        directoriesToMove=directories,
    )

def print_green(info) -> None:
    print(GREEN + info + RESET)


def main(config_name) -> None:
    path_to_config = os.getcwd() + CONFIGS_DIRECTORY + "/" + config_name + "/config.json"
    config = load_config(Path(path_to_config))
    print_green("Beginning Setup for config " + config.name)
    for service in config.services:
        print_green("Halting service " + service)
        subprocess.run(["systemctl", "stop", service])
    for package in config.packages:
        print_green("Installing/Updating package " + package + " if needed")
        subprocess.run(["apt", "install", package])
    for directory in config.directoriesToMove:
        source_directory = os.getcwd() + CONFIGS_DIRECTORY + "/" + config_name + "/files/" + directory.source
        print_green("Copying directory " + source_directory + " to " + directory.destination)
        subprocess.run(["rsync", "--delete", "-o", config.metadata.owner, "-g", config.metadata.group, source_directory, directory.destination])
        subprocess.run(["chmod", config.metadata.mode, "-R", directory.destination])
    for service in config.services:
        print_green("Starting Service " + service)
        subprocess.run(["systemctl", "start", service])
        subprocess.run(["systemctl", "status", service])



    return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        "TODO add usage information"
        sys.exit(1)
    main(sys.argv[1])

