#!/bin/sh
RELEASE_PATH="./Deployment/Release"
GIT_INFO_PATH="./git_info.json"
REPO="$(basename -s .git `git config --get remote.origin.url`)"
VERSION="$(git describe  --abbrev=7 --tags --always --first-parent)"
BRANCH="$(git rev-parse HEAD)"
CONFIG=`echo $VERSION | sed -E 's/.*_V([[:digit:].]+)*/\1/'`

# variables
base_image_token="{{ image_tag }}" # find all these...
image_tag=$VERSION

base_branch_token="{{ branch_name }}" # find all these...
branch_name=$BRANCH

repo_name_token="{{ repo_name }}" # find all these...
repo_name=$REPO

base_config_token="{{ config_version }}" # find all these...

rm -rf $RELEASE_PATH/docker-compose.yml

# find and replace
sed -e "s/${base_image_token}/${image_tag}/g" \
    < $RELEASE_PATH/docker-compose-template.yml \
    > $RELEASE_PATH/docker-compose.yml

# include parse_yaml function
. $RELEASE_PATH/parse_yaml.sh

# read yaml file
eval $(parse_yaml $RELEASE_PATH/docker-compose.yml "config_")
image_name_key_str=${config_services_}_image
image_name_key="$(echo -e "${image_name_key_str}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
export IMAGE_NAME="${!image_name_key}"

container_name_key_str=${config_services_}_container_name
container_name_key="$(echo -e "${container_name_key_str}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
export CONTAINER_NAME="${!container_name_key}"

rm -rf $GIT_INFO_PATH

# find and replace
sed -e "s/${base_image_token}/${image_tag}/g" \
-e "s/${base_branch_token}/${branch_name}/g" \
-e "s/${base_config_token}/${CONFIG}/g" \
-e "s/${repo_name_token}/${repo_name}/g" \
    < $RELEASE_PATH/git_info_template.json \
    > $GIT_INFO_PATH

docker build -t ${IMAGE_NAME} -f Docker/Dockerfile .
docker push ${IMAGE_NAME}
docker image rm ${IMAGE_NAME}
