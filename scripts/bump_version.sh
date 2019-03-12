set -x
cd `dirname $0`
cd ../src

git checkout master

version=`cat VERSION`

docker create -v /app --name configs alpine:3.4 /bin/true
docker cp . configs:/app

docker run  --volumes-from configs --name bumper treeder/bump  patch
docker cp bumper:/app/VERSION VERSION


# ssh-add -D
# ssh-keyscan github.com >> githubKey
# ssh-keygen -lf githubKey
# cat githubKey >> ~/.ssh/known_hosts



version=`cat VERSION`

git add VERSION
git commit -m "version $version"
git tag  "$version"
git push  https://${GITHUB_PERSONAL_TOKEN}@github.com/remorses/instagram-botnet.git --tags
