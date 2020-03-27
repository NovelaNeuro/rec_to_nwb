DOC_REPO='https://github.com/NovelaNeuro/fldatamigration-docs'

echo 'README.md copying to docs/source and removing first line'
tail -n +2  README.md >  README.tmp && mv  README.tmp docs/source/README.md

echo 'Create HTML Documentation'
make html -C ./docs

#echo 'Deploy documentation to' $DOC_REPO
#

echo 'Click enter to exit'
read exitKey