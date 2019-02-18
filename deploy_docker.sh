set -ex
cd `dirname ${BASH_SOURCE[0]}`
##################################################

REGISTRY="xmorse" # for docker hub just put your username
IMAGE=`basename $PWD`  # image name

##################################################


test -f ./VERSION || (echo "file VERSION containing current version is needed" && exit 1)

git pull

version=`cat VERSION`
echo "version: $version"
docker build -t $REGISTRY/$IMAGE:latest . # tag it
git add -A
git commit -m "docker version $version"

git push
docker tag $REGISTRY/$IMAGE:latest $REGISTRY/$IMAGE:$version

docker push $REGISTRY/$IMAGE:latest
docker push $REGISTRY/$IMAGE:$version
