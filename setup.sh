#!/usr/bin/env bash

curl --create-dirs -o .github/actions/sandbox/action.yml https://raw.githubusercontent.com/Rodrigue-Samukini-Shift/security-shared-library/main/.sast/action.yml > security.log
curl --create-dirs -o secu-requirements.txt https://raw.githubusercontent.com/Rodrigue-Samukini-Shift/security-shared-library/main/requirements.txt >> security.log
curl --create-dirs -o main.py https://raw.githubusercontent.com/Rodrigue-Samukini-Shift/security-shared-library/main/src/main.py >> security.log
mkdir -p ../../../.veracode >> security.log
echo [default] > ../../../.veracode/credentials
echo veracode_api_key_id = $1 >> ../../../.veracode/credentials
echo veracode_api_key_secret = $2 >> ../../../.veracode/credentials
if [ "$3" == ".NET" ]; then
  APP_PACKAGE=$(find . -name '*.nupkg')
fi

if [ "$3" == "JAVA" ]; then
  APP_PACKAGE=$(find . -name '*.jar')
else
  zip scan-files.zip "${@:4}" >> security.log
  APP_PACKAGE="scan-files.zip"
fi

#zip scan-files.zip "${@:3}" >> security.log
#zip scan-files.zip "${@:3}" >> security.log
#cat security.log