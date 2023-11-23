#!/usr/bin/env bash

curl --create-dirs -o .github/actions/create-sandbox/action.yml https://raw.githubusercontent.com/Rodrigue-Samukini-Shift/security-shared-library/main/.sast/action.yml > security.log
curl --create-dirs -o secu-requirements.txt https://raw.githubusercontent.com/Rodrigue-Samukini-Shift/security-shared-library/main/requirements.txt >> security.log
curl --create-dirs -o create-application-version.py https://raw.githubusercontent.com/Rodrigue-Samukini-Shift/security-shared-library/main/src/create-application-version.py >> security.log
mkdir -p ../../../.veracode >> security.log
echo [default] > ../../../.veracode/credentials
echo veracode_api_key_id = $1 >> ../../../.veracode/credentials
echo veracode_api_key_secret = $2 >> ../../../.veracode/credentials
zip scan-files.zip \"$3\" >> security.log
cat security.log