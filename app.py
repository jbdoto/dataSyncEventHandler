import json
import os

import boto3

print('Loading function')
datasync_client = boto3.client('datasync')
step_client = boto3.client('stepfunctions')


def handle_event(event, context):
    try:
        print("Received event: " + json.dumps(event, indent=2))

        # grab resources section of event, get task execution ids
        task_execution_arns = event['resources']

        # now fetch the input filter info from each task_detail, fire off jobs
        new_files_to_process = []
        for task_execution_arn in task_execution_arns:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_task_execution
            response = datasync_client.describe_task_execution(TaskExecutionArn=task_execution_arn)
            print("Task execution details: " + str(response))
            # this will be the location of the data in configured s3 bucket:
            # 'Includes': [
            #         {
            #             'FilterType': 'SIMPLE_PATTERN',
            #             'Value': 'string'
            #         },
            #     ]
            if len(response['Includes']) > 0:
                file = response['Includes'][0]['Value']
                # files typically start with leading '/', strip that leading '/'
                print("Got filename:" + file)
                if file.startswith('/', 0):
                    new_files_to_process.append(file.lstrip('/'))
                else:
                    new_files_to_process.append(file)
            else:
                print("Response didn't contain Includes files...")

        if len(new_files_to_process) == 0:
            print('No files were parsed from input...exiting')
            return

        for new_file_to_process in new_files_to_process:
            state_machine_arn = os.environ['STATE_MACHINE_ARN']
            payload = {"ObjectName": new_file_to_process}
            json_payload = json.dumps(payload)
            print('Starting bcl2fastq with payload %s' % json_payload)
            #
            response = step_client.start_execution(stateMachineArn=state_machine_arn, input=json_payload)
            print(response)

    except Exception as e:
        print(e)
        print('Error handling event. %s' % e)
        raise e
