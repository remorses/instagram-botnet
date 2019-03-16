
cd `dirname $0`
cd ../src

git checkout master

git pull https://${GITHUB_PERSONAL_TOKEN}@github.com/remorses/instagram-botnet.git

version=`cat VERSION`

docker create -v /app --name configs alpine:3.4 /bin/true
docker cp . configs:/app

docker run  --volumes-from configs --name bumper treeder/bump  patch
docker cp bumper:/app/VERSION VERSION


# ssh-add -D
# ssh-keyscan github.com >> githubKey
# ssh-keygen -lf githubKey
# cat githubKey >> ~/.ssh/known_hosts

git config user.name "Tommaso De Rossi"
git config user.email "beats.by.morse@gmail.com"


version=`cat VERSION`

git add VERSION
git commit -m "[skip ci] version $version"
git tag  -a "$version" -m "[skip ci]"
git push --tags  https://${GITHUB_PERSONAL_TOKEN}@github.com/remorses/instagram-botnet.git  HEAD --no-verify
