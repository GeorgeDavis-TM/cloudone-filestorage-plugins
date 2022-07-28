# Cloud One File Storage Security Post Scan Action for GCP - Email notifications

## Overview

<walkthrough-tutorial-duration duration="10"></walkthrough-tutorial-duration>

This tutorial will guide you to deploy a Google Cloud function to push Email notifications.

## Project Setup

Copy the execute the script below to set the project ID where the storage stack is deployed.

<walkthrough-project-setup></walkthrough-project-setup>

> If using a local machine and not Google Cloud Shell, use `gcloud auth application-default login` to login with gcloud CLI.

```
gcloud config set project <walkthrough-project-id/>
```

## Deploy Google Cloud function to push Email notifications

<!-- TODO: Use params to substitute CLI and Stage parameters using inheritance and overriding -->
1. Setup the serverless.yml file with your `environment` variables, like `MAIL_FROM`, `MAIL_TO`, `MAIL_SUBJECT`, `MAIL_SERVER`, `MAIL_LOCAL_HOST`, `MAIL_FORCE_TLS`, `MAIL_DEBUG`.

2. Deploy Serverless project

    ```
    serverless plugin install -n serverless-google-cloudfunctions
    serverless deploy -s prod
    ```

3. Check your email client to see new email notifications. For testing the plugin, download an EICAR file and upload the file to your Google Cloud Storage bucket. [Download EICAR file here](https://secure.eicar.org/eicar_com.zip)
