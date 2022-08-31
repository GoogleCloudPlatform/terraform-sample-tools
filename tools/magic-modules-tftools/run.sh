#!/bin/bash
cleanup () {
  # Clear MAC OS cache files
  find . | grep -E "(.DS_Store)" | xargs rm -rf
  # Clearn Python cache files
  find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
  rm -rf dist/ build/ .nox/ .pytest_cache/ tftools.egg-info/ tests/sponge_log.xml
  rm -rf test/sponge_log.xml test/__pycache__ __pycache__
  clear
  echo "Cleanup completed"
}

update_dockerhub_image () {
  cleanup
  docker build -t tftools:latest .
  docker tag tftools:latest msampathkumar/tftools:`date +'%Y%m%d'`
  docker tag tftools:latest msampathkumar/tftools:latest
  docker push msampathkumar/tftools:latest
  docker push tftools:latest msampathkumar/tftools:`date +'%Y%m%d'`
}

install_tftools () {
  cleanup
  python3 setup.py install
}

#############################################################
####### From CLI, you can run the following commands` #######
#############################################################
#. ./run.sh && cleanup
#. ./run.sh && update_dockerhub_image
#. ./run.sh && install_tftools

# install_tftools

# basic test
#cd tests
#pytest -v
#cd ..

# final test: multi-version test
 nox

