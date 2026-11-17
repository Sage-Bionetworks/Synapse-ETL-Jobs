# Synapse-ETL-Jobs
[AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html) is a cloud service that prepares data for analysis 
through automated extract, transform and load (ETL) processes. The Glue job uses the scripts for the ETL process. 
The Synapse-ETL-Jobs project maintains all the Python-based Glue job scripts. The Glue jobs are responsible for moving 
Synapse warehouse json data to S3 in parquet format, which can be queried by Athena. The [Synapse-Stack-Builder](https://github.com/Sage-Bionetworks/Synapse-Stack-Builder) 
project deploys these Python scripts to s3 and creates the Glue jobs. For more information please see 
the [design documentation](https://sagebionetworks.jira.com/wiki/spaces/DW/pages/2732916846/Processing+Access+Records+using+AWS+High+Level+Design).

# Repository structure
This repository contains the Python scripts, which are only used by Glue jobs.

### `src/`
This directory contains the Glue job scripts.

### `tests/`
This directory contains the unit tests for Glue job scripts.

### `.github/`
This directory contains the scripts for GitHub Actions.

# Local Python setup
The project's scripts are Python-based. In order to make use of Python libraries and address syntax errors, 
it's essential to have Python 3 installed, as Glue employs Python 3.

```
brew install python@3.10
```

# Local test environment setup
In order to execute the tests, the presence of Glue libraries is necessary. To address the dependencies related to Glue, 
build a Docker container using the AWS Glue image to ensure the provisioning of essential prerequisites.

1. Install and start Docker. If you’re on Mac, you can download and install Docker Desktop (https://www.docker.com/products/docker-desktop). 
Note that you’ll need to create a Docker account.
2. Create a Docker project directory for your AWS Glue container. Name could be like ~/docker/AWSGlue
3. In that directory, create a file called docker-compose.yml. Its contents should contain
```
version: '3.3'
services:
    aws-glue:
        image: aws-glue
        container_name: 'aws-glue'
        ports:
          - 8888:8888
          - 4040:4040
```
4. In the same directory, run docker-compose up -d. This will launch a Docker container with the image.

If you already have a docker container, run the following command to build the image.
```
docker build -t aws-glue .
```

To initiate tests, run the following command, which will execute the test files prefixed with 'test'.

```
docker run -v ~/.aws:/home/glue_user/.aws -v  ${LOCAL_WORKSPACE ../SageBionetworks/Synapse-ETL-Service}:/home/glue_user/workspace/  -e DISABLE_SSL=true --rm -p 4040:4040 -p 8888:8888  aws-glue -c "python3 -m pytest"
```

# GitHub Actions

1. python-package.yml : This action sets up the Python environment, installs dependencies and checks syntax errors 
or undefined references. Furthermore, it builds the docker image and executes the tests.

2. tag_release.yml : A GitHub action to automatically `bump` and `tag` develop branch, on merge, with the latest 
SemVer formatted (Major.Minor.Patch) version. If no version is provided, the `Minor` field is bumped.
The desired bump can be specified in the commit message, e.g. with `#major`, `#minor`, or `#patch`.  For more information,
please see the [documentation](https://github.com/anothrNick/github-tag-action).
