set -ex
cd `dirname $0`
cd ../src

test -f ./VERSION || (echo "file VERSION containing current version is needed" && exit 1)

version=`cat VERSION`

echo $DOCKERUSERNAME/instagram-botnet:$version

docker build -t $DOCKERUSERNAME/instagram-botnet:latest ../

docker tag $DOCKERUSERNAME/instagram-botnet:latest $DOCKERUSERNAME/instagram-botnet:$version

docker push $DOCKERUSERNAME/instagram-botnet:latest

docker push $DOCKERUSERNAME/instagram-botnet:$version

docker login -u $DOCKERUSERNAME -p $DOCKERPASSWORD
