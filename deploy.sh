set -ex
cd `dirname ${BASH_SOURCE[0]}`

./deploy_pypi.sh
./deploy_docker.sh
