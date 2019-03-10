
cd `dirname $0`
cd ../src

version=`cat VERSION`

docker create -v /app --name configs alpine:3.4 /bin/true
docker cp . configs:/app

docker run  --volumes-from configs --name bumper treeder/bump  patch
docker exec bumper ls -1 /app
docker cp bumper:/app/VERSION VERSION


git config credential.helper 'cache --timeout=120'
git config user.email $GITHUBEMAIL
git config user.name $GITHUBPASSWORD

ssh-keyscan github.com >> githubKey
ssh-keygen -lf githubKey
cat githubKey >> ~/.ssh/known_hosts

git checkout master
git status

version=`cat VERSION`

git add VERSION
git commit -m "version $version"
git tag -a "$version" -m "version $version"
git push -u origin master
