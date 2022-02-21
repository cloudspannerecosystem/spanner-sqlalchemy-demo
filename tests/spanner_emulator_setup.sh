gcloud config configurations create emulator
gcloud config set auth/disable_credentials true
gcloud config set project your-project-id
gcloud config set api_endpoint_overrides/spanner http://localhost:9020/
gcloud spanner instances create demo  --config=emulator-config --description="Test Instance" --nodes=1
gcloud spanner databases create ranking --instance=demo
