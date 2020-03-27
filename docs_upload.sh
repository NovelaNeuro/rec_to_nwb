DOC_REPO='https://github.com/NovelaNeuro/fldatamigration-docs'

echo 'README.md copying to docs/source and removing first line'
tail -n +2 README.md > README.tmp && mv README.tmp docs/source/README.md

echo 'LICENSE.md copying to docs/source and adding first line'
cp LICENSE.md ./docs/source/
sed -i '1i License' ./docs/source/LICENSE.md && sed -i '2i ===================' ./docs/source/LICENSE.md

echo 'Creating API Documentation'
sphinx-apidoc -fMET ./fl/datamigration -o ./docs/source/autoapi

echo 'Create HTML Documentation'
make html -C ./docs

#echo 'Deploy documentation to' $DOC_REPO docs/source
# maybe this? https://github.community/t5/How-to-use-Git-and-GitHub/Adding-a-folder-from-one-repo-to-another/td-p/5425
# git subtree push --prefix=docs\source &DOC_REPO master
# https://gist.github.com/Maumagnaguagno/84a9807ed71d233e5d3f


echo 'Click enter to exit'
read exitKey