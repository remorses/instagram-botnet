set -ex
cd `dirname $0`
cd ../src


git config credential.helper 'cache --timeout=120'
git config user.email $GITHUBEMAIL
git config user.name $GITHUBPASSWORD

git checkout master
git status
git branch master
git add VERSION
git commit -m "version $version"
git tag -a "$version" -m "version $version"
git push
