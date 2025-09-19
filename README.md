# Server-Setup-Tool
Sever-setup-tool is a configuration based tool that can help you deploy `systemd` based services on Ubuntu. This tool supports starting and stopping services, downloading and updated selected packages via `apt`, deployment of configuration files needed for the service to operate, and the setting of ownership, groups and permissions. This tool is **idempotent** and can be run without issue, although it will interrupt the operating of running services if invoked for the duration of the tool's execution.


# Usage

- Checkout from Git Repo on an Ubuntu server
- Create configuration for your service (see Configuration section)
- Execute `python3 setuptool.py config_name` where `config_name` is the name of your configuration (the attached example can be run using `python3 setuptool.py phpserver`

**Note**: user must have `root` access to run this tool

## Configuration
To create a new configuration
1. Create a new directory under the `config` directory. The name of this directory will be the name of your configuration
2. Create a file `config.json` in this directory that will hold the configuration details
3. Create a directory `/files` under the directory for your configuration. This will hold files necessarily for your service, and you will be able to specify what files to deploy where inside of the configuration

Attached in this repository in the `phpserver` is an example config for a deployment of a php based service on `apache`

    {
        "name": "phpserver",
        "description": "A simple PHP server configuration",
        "version": "1.0.0",
        "metadata":
            {
               "owner": "root",
               "group": "root",
               "mode": "755"
            },
        "services": ["apache2"],
        "packages": ["apache2", "libapache2-mod-php"],
        "directoriesToMove": [
            {
                "source": "html",
                "destination": "/var/www"
            }
        ]
    }
   - **Name**: The name of your configuration, this should be a `string` matching the name of the directory this configuration lives in
   - **Description**: A brief `string` description of what the configuration aims to do
   - **Version**: A `string` for keeping track of versioning if desired
   - **Metadata**: An `object` containing fields pertaining to permissioning for files
	   - **Owner**: `string` of the owner of the file
	   - **Group**`string` of the group associated with the file
	   - **Mode** [Chmod octal notation](https://docs.oracle.com/cd/E19504-01/802-5750/6i9g464pv/index.html) for permissions that should be attached to files
- **Services**: Array of `string` names of services that are being affected by this configuration. These services will be stopped at the start of execution, than restarted at the end
- **Packages**: Array of `string` names of packages that need to  be downloaded or updated via apt 
- **DirectoriesToMove**: Array of `Object` representing directories that need to be copied. This tool will take what is in the each `source` directory specified, and drop it in its entirety to `destination`
	- **Source**: `string` name of a directory inside the `files` directory
	- **Destination**`string` target destination.
   

## Architecture
- Tool is written in Python and lives entirely within `setuptool.py`
- Configuration is JSON based and parsed inside the python tool
- Operations are all shelled out for simplicity
	- `systemd`  to stop the services that need updating (if applicable)
	- `apt` to download/update required packages
	- `rsync` to copy files needed by service over to target directories 
	- `chown` and `chmod` to set ownership, group and permission for files
	- `systemd`  to restart services


## Future Improvements
- There is not sufficient error handling yet for invalid paths being passed in
- The tool currently requires paths to be passed in in a very specific way. Making it more tolerant to different ways of expressing filepaths would be a large quality of life change
- Having the tool have an additional mode to generate the skeleton of a configuration would largely reduce the chances of having malformed configurations
- Group/Ownership/Mode would ideally be able to be specified on a per file basis
- Some operations could be done natively inside python for more control 

