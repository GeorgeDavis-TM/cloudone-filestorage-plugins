# Cloud One File Storage Security Post Scan Action for GCP - Email notifications

**:warning: Note: File Storage Security for GCP solution is in preview.**

## Prerequisites

1. **Install supporting tools**
   - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk)

## Installation

### With GCP Cloud Shell

1. Visit [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Ftrendmicro%2Fcloudone-filestorage-plugins.git&cloudshell_workspace=post-scan-actions%2Fgcp-python-email-notification&cloudshell_tutorial=docs/deploy-tutorial.md)

### LocalMachine

1. Login to the Google Cloud SDK

   ```sh
   gcloud init
   ```

2. Copy the execute the script below to set the project ID where the storage stack is deployed.

> If using a local machine and not Google Cloud Shell, use `gcloud auth application-default login` to login with gcloud CLI.

   ```
   gcloud config set project <walkthrough-project-id/>
   ```

<!-- TODO: Use params to substitute CLI and Stage parameters using inheritance and overriding -->
3. Setup the serverless.yml file with your `environment` variables, like `MAIL_FROM`, `MAIL_TO`, `MAIL_SUBJECT`, `MAIL_SERVER`, `MAIL_LOCAL_HOST`, `MAIL_FORCE_TLS`, `MAIL_DEBUG`.

4. Deploy Serverless project

    ```
    serverless plugin install -n serverless-google-cloudfunctions
    serverless deploy -s prod
    ```

5. Check your email client to see new email notifications. For testing the plugin, download an EICAR file and upload the file to your Google Cloud Storage bucket. [Download EICAR file here](https://secure.eicar.org/eicar_com.zip)
