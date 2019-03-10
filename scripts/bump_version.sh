set -ex
cd `dirname $0`
cd ../src

version=`cat VERSION`

docker create -v /app --name configs alpine:3.4 /bin/true
docker cp . configs:/app

docker run --rm  --volumes-from configs treeder/bump patch


git config credential.helper 'cache --timeout=120'
git config user.email $GITHUBEMAIL
git config user.name $GITHUBPASSWORD

git checkout master
git status

git add VERSION
git commit -m "version $version"
git tag -a "$version" -m "version $version"
git push
