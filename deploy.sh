set -ex
cd `dirname $0`
echo $BASH_SOURCE[0]
echo $PWD

./deploy_pypi.sh
./deploy_docker.sh
