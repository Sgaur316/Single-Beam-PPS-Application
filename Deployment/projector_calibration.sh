#!/usr/bin/env/ bash


calibrationFunc()
{
   echo "Starting Projector in Calibration Mode...."
   mode=calibration docker-compose -f ./docker-compose_projector.yml up -d
   docker attach projectorservice
}


image_tags=$(sudo docker image ls --format "{{.Repository}}:{{.Tag}}")
imageArray=(`echo $image_tags | sed 's/ /\n/g'`)
IMAGE_NUM=1
for image_tag in $image_tags 
do 
# echo "$IMAGE_NUM: $image_tag"
if grep -q "projector" <<< "$image_tag"; then
   echo "Generating Projector docker-compose.yml file"
   docker run --rm --entrypoint cat $image_tag /docker-compose.yml > ./docker-compose_projector.yml
   docker-compose -f ./docker-compose_projector.yml down
   calibrationFunc
   break
fi
done
