set -ex
cd `dirname $0`
cd ../src

version=`cat VERSION`

docker create -v /app --name configs alpine:3.4 /bin/true
docker cp . configs:/app

docker run --rm  --volumes-from configs treeder/bump patch
