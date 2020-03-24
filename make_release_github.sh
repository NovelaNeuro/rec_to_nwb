#!/bin/bash

read_prerelease() {
  echo "Pre-release? [y/n]: "
  read is_prerelease
  if [ $is_prerelease == "y" ]; then
    is_prerelease="true"
  elif [ $is_prerelease == "n" ]; then
    is_prerelease="false"
  else
    read_prerelease
  fi
}

read_draft() {
  echo "Draft? [y/n]: "
  read is_draft
  if [ $is_draft == "y" ]; then
    is_draft="true"
  elif [ $is_draft == "n" ]; then
    is_draft="false"
  else
    read_draft
  fi
}

generate_post_data() {
cat <<EOF
{

  "tag_name": "$versionLabel",
  "target_commitish": "$masterBranch",
  "name": "$title",
  "body": "",
  "draft": $is_draft,
  "prerelease": $is_prerelease

}
EOF
}

branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

projectName="$(git config --get remote.origin.url | cut -d/ -f5 | cut -d. -f1)"
repoFullName=$(git config --get remote.origin.url | sed 's/.*:\/\/github.com\///;s/.git$//')

# Personal access token, set by command: git config --global github.token XXXXXXXXXXXXXXXXX
token=$(git config --global github.token)

masterBranch=master

git checkout $masterBranch

if [ $branch == "master" ]; then

#  It takes stdout from print in setup. It will throw an error, but that is ok. python setup.py --version use normalization that change 0.0.001 to 0.0.1.
  versionNumber=$(python setup.py)
  versionLabel=v$versionNumber
  releaseBranch=master_release
  title=$versionLabel

  read_draft
  read_prerelease

  echo "Delete old branch $releaseBranch ....."
  git branch -d master_release
  git push origin --delete master_release

  git checkout $masterBranch

  echo "Started releasing $versionLabel for $projectName ....."

  git pull

 response=$(curl -o /dev/null -s -w "%{http_code}\n" --data "$(generate_post_data)"  "https://api.github.com/repos/$repoFullName/releases?access_token=$token")

  if [ $response == 201 ]; then
    echo "$versionLabel is successfully released for $projectName !"

    git checkout -b $releaseBranch $masterBranch

    git checkout $masterBranch

    git push -u origin $releaseBranch

    git checkout $masterBranch

    git pull

    echo "Bye!"
  else
    echo "Something went wrong, code $response"
    echo "Check if the release does not exist already"
  fi

else
  echo "Please make sure you are on master branch and come back!"
  echo "Bye!"
fi

echo "Click 'Enter' to exit"
read _
