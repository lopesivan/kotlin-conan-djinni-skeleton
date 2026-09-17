#!/usr/bin/env bash
set -e # Encerra em caso de erro
set -u # Trata variáveis não definidas como erro
set -o pipefail

n=projeto
m=project

o=01-projeto
d=02-projeto

rm -rf $d
cp -r $o $d

find $d/ -type f -exec grep -l projeto01 {} + |
    xargs -I{} sed "s/projeto01/projeto02/g" -i {}

find $d/ -type f -exec grep -l project01_ {} + |
    xargs -I{} sed "s/project01_/project02_/g" -i {}

find $d/ -type f -exec grep -l PROJECT01_ {} + |
    xargs -I{} sed "s/PROJECT01_/PROJECT02_/g" -i {}

find $d/ -type f -exec grep -l "Projeto 01" {} + |
    xargs -I{} sed "s/Projeto 01/Projeto 02/g" -i {}

pushd ${d}/src/main/java/br/eng/ivanlopes
mv projeto01/ projeto02
popd

exit 0
