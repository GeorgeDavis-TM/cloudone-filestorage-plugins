import json
import os
import sendmail

def lambda_handler(event, context):

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

    for record in event['Records']:

        # Analyze the message and look for findings
        message = json.loads(record['Sns']['Message'])
        findings = message['scanning_result'].get('Findings')

        if findings:

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
                <html><head></head><body><h1>CloudOne FSS Email Notification</h1><p>
                <p><b>File URL: </b>{file_url}</p>\
                '''.format(file_url=str(message['file_url']))
            for finding in message['scanning_result']['Findings']:
                body_html = body_html + '''\
                    <p><b>Malware: </b>{malware}</p>
                    <p><b>Type: </b>{type}</p>
                    </html></body></p>\
                    '''.format(malware=str(finding.get('malware')), type=str(finding.get('type')))

            mailDict.update({"mailMessageBody": body_html})

            # Try to send the email.
            try:
                response = sendmail.pubsub_sendmail(mailDict=mailDict, context=context)
            # Display an error if something goes wrong.
            except Exception as e:
                print(e)
                return
            else:
                print("Email sent! Message ID:" + response['MessageId'])
                return

    print("Nothing done.")
