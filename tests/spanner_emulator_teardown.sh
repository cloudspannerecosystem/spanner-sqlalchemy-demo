#!/bin/bash

docker stop spanner-emulator
gcloud config unset auth/disable_credentials
gcloud config unset api_endpoint_overrides/spanner
gcloud config configurations activate default
gcloud config set core/project kzs-sandbox
