set -ex
cd `dirname ${BASH_SOURCE[0]}`
echo $PWD

./deploy_pypi.sh
./deploy_docker.sh
