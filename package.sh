#!/bin/bash
#================================================================
# HEADER
#================================================================
#%
#% DESCRIPTION
#%    This is a script to create package for Projector Experiments Application using FPM utility
#%    
#%
#================================================================
#- IMPLEMENTATION
#-    version         ${SCRIPT_NAME} (www.greyorange.com) 0.0.1
#-    author          Shivam Sood
#-    copyright       Copyright (c) http://www.greyorange.com
#-
#================================================================
#
#================================================================
# END_OF_HEADER
#================================================================

#============================
#  FUNCTIONS
#============================

check_fpm()
{

if ! gem spec fpm > /dev/null 2>&1; then
  echo "Error###################"
  echo "Gem fpm is not installed!"
  echo "Read about using FPM here : https://www.digitalocean.com/community/tutorials/how-to-use-fpm-to-easily-create-packages-in-multiple-formats";
  echo "Make sure you have pip installed as well!!!."
  exit 1
fi

}
 
 
#============================
#  FILES AND VARIABLES
#============================

NAME="projector_experiment"
VERSION="$(git describe --dirty --abbrev=7 --tags --always --first-parent)"
BUILD_DIR="build_files"
AFTER_INSTALL="dpkg/after_install.sh"
AFTER_REMOVE="dpkg/after_remove.sh"
DEPS_CACHE="deps_cache"

#============================
#  MAIN SCRIPT
#============================

check_fpm

rm -f *.deb
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}/opt/projector_experiment"
mkdir -p "${BUILD_DIR}/etc/supervisor/conf.d"
mkdir -p "${DEPS_CACHE}"

pip install --download "${DEPS_CACHE}" -r requirements.txt


# Copy files/folders to the required locations
cp -r {action_queue.py,app.py,calibration.py,config.py,corner_points.cfg,logger.py,projection.py,usb_detector.py,"${DEPS_CACHE}",requirements.txt} "${BUILD_DIR}/opt/projector_experiment/"
cp dpkg/projector_experiment.conf "${BUILD_DIR}/etc/supervisor/conf.d/"

fpm -s dir -t deb --after-install "${AFTER_INSTALL}" --after-remove "${AFTER_REMOVE}" \
    -d 'python' -d 'libpq-dev' -d 'virtualenv' -d 'python-dev' -d 'python-pip' -d 'supervisor' -d 'libffi-dev' \
    -d 'supervisor' -a all -n "${NAME}" -v "2${VERSION}" \
    -m "Grey Orange <packages@greyorange.sg>" build_files/=/

#============================
# CLEANUP
#============================

rm -rf ${BUILD_DIR}

