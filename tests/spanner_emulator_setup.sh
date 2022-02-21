gcloud spanner instances create demo  --config=emulator-config --description="Test Instance" --nodes=1
gcloud spanner databases create ranking --instance=demo
