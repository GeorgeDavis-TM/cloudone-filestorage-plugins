import os
import json
import base64
import pubsub_sendmail

def get_gcp_project_id(resource_name):
    return str(resource_name).split("/")[1]

def get_bucket_name_from_file_url(file_url):
    return str(file_url.split("/")[-2:][0])

def get_file_name_from_file_url(file_url):
    return str(file_url.split("/")[-1:][0])

def build_file_metadata_url(project_id, bucket_name, file_name):
    return "https://console.cloud.google.com/storage/browser/_details/" + bucket_name + "/" + file_name + "?project=" + project_id

def main(event, context):

    try:

        print(f'Context: {context}')
        print(f'Event: {event}')
        base64_data = event.get('data', '')
        base64_bytes = base64_data.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = json.loads(message_bytes.decode('ascii'))
        print(f'Message: {message}')

        print("""This Function was triggered by messageId {} published at {} to {}""".format(context.event_id, context.timestamp, context.resource))

        mailFrom      = os.environ.get('MAIL_FROM', '').strip()
        mailTo        = os.environ.get('MAIL_TO', '').strip()
        mailSubject   = os.environ.get('MAIL_SUBJECT', '').strip()
        mailServer    = os.environ.get('MAIL_SERVER', '').strip()
        mailLocalHost = os.environ.get('MAIL_LOCAL_HOST', '').strip()
        mailForceTls  = os.environ.get('MAIL_FORCE_TLS', '').strip()
        mailDebug     = os.environ.get('MAIL_DEBUG', '').strip()
        # charset = "UTF-8"

        mailDict = {}
        mailDict.update({"mailFrom": mailFrom})
        mailDict.update({"mailTo": mailTo})
        mailDict.update({"mailSubject": mailSubject})
        mailDict.update({"mailServer": mailServer})
        mailDict.update({"mailLocalHost": mailLocalHost})
        mailDict.update({"mailForceTls": mailForceTls})
        mailDict.update({"mailDebug": mailDebug})

        if message:
            # Message details from the Pub/Sub topic publish event
            findings = message['scanning_result'].get('Findings')

            if findings:

                project_id = get_gcp_project_id(resource_name=context.resource)
                bucket_name = get_bucket_name_from_file_url(file_url=str(message['file_url']))
                file_name = get_file_name_from_file_url(file_url=str(message['file_url']))

                # body_text = '''\
                #     CloudOne FSS Email Notification
                #     File URL: {file_url}\
                #     '''.format(file_url=str(message['file_url']))
                # for finding in message['scanning_result']['Findings']:
                #     body_text = body_text + '''\
                #         Malware: {malware}
                #         Type: {type}\
                #         '''.format(malware=str(finding.get('malware')), type=str(finding.get('type')))

                body_html = '''\
                        <html><head></head><body><h1>Cloud One FSS Email Notification</h1><p>
                        <p><b>GCP Project ID: </b>{project_id}</p>
                        <p><b>GCP Bucket Name: </b>{bucket_name}</p>
                        <p><b>File Name: </b>{file_name}</p>
                    '''.format(
                        project_id=project_id,
                        bucket_name=bucket_name,
                        file_name=file_name
                    )
                for finding in message['scanning_result']['Findings']:
                    body_html = body_html + '''\
                        <p><b>Malware Name(s): </b>{malware}</p>
                        <p><b>Malware Type(s): </b>{type}</p>
                        <p><b>File URL: </b>{file_metadata_url}</p>
                        </html></body></p>\
                        '''.format(
                            malware=str(finding.get('malware')),
                            type=str(finding.get('type')),
                            file_metadata_url=str(build_file_metadata_url(project_id=project_id, bucket_name=bucket_name, file_name=file_name))
                        )

                mailDict.update({"mailMessageBody": body_html})

                # Try to send the email.
                try:
                    response = pubsub_sendmail.pubsub_sendmail(mailDict=mailDict, context=context)
                # Display an error if something goes wrong.
                except Exception as e:
                    print(e)
                    return
                else:
                    print("Email sent! Message ID:" + response['MessageId'])
                    return

    except Exception as e:
        print("Error: ", str(e))

    print("Nothing done.")
