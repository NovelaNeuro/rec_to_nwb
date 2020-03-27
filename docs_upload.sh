DOC_REPO='https://github.com/NovelaNeuro/fldatamigration-docs'

echo 'README.md copying to docs/source and removing first line'
tail -n +2 README.md > README.tmp && mv README.tmp docs/source/README.md

echo 'LICENSE.md copying to docs/source and adding first line'
cp LICENSE.md ./docs/source/
sed -i '1i License' ./docs/source/LICENSE.md && sed -i '2i ===================' ./docs/source/LICENSE.md

echo 'Creating API Documentation'
sphinx-apidoc -o ./docs/source/autoapi ./fl/datamigration

#echo ' Autodoc? '
#sphinx-autodoc

echo 'Create HTML Documentation'
make html -C ./docs

#echo 'Deploy documentation to' $DOC_REPO
#

echo 'Click enter to exit'
read exitKey