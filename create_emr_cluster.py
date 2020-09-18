import json
import boto3

def lambda_handler(event, context):

    print('Loading function')

    print("Starting ..")
    client = boto3.client('emr',  region_name="eu-west-1")

    instances = {
                'MasterInstanceType': 'm3.xlarge',
                'SlaveInstanceType': 'm3.xlarge',
                'InstanceCount': 1,
                'InstanceGroups': [],
                'Ec2KeyName': 'spark',
                'KeepJobFlowAliveWhenNoSteps': True,
                'TerminationProtected': False,
                'Ec2SubnetId': 'subnet-b51b2fd3',
                'EmrManagedMasterSecurityGroup': 'sg-00e712ec1b09f676e',
                'EmrManagedSlaveSecurityGroup':  'sg-0e9ebbfd18d0669a8'
            }
    configurations = [
        {
            'Classification':'yarn-site',
            'Properties':{
                'yarn.resourcemanager.scheduler.class':'org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler'
            },
            'Configurations':[]
        },
        {
            "Classification": "spark-env",
            "Configurations": [
                {
                    "Classification": "export",
                    "Properties": {
                        "PYSPARK_PYTHON": "/usr/bin/python3"
                    }
                }
            ]
        }
    ]

    #--------------------------------------------------------------------------
    #Create EMR Cluster with client.run_job_flow API and get the reponse
    #--------------------------------------------------------------------------
    response = client.run_job_flow (
        Name='PySpark Cluster',
        LogUri='s3://aws-logs-788660014500-eu-west-1/emr-logs',
        ReleaseLabel='emr-5.30.0',
        Instances=instances,
        Configurations=configurations,
        Steps=[],
        BootstrapActions=[],
        Applications=[
            {'Name': 'Spark'},
            {'Name': 'Zeppelin'},
            {'Name': 'Ganglia'}
        ],
        VisibleToAllUsers=True,
        ServiceRole='EMR_DefaultRole',
        JobFlowRole='EMR_EC2_DefaultRole',
        AutoScalingRole='EMR_AutoScaling_DefaultRole',
        EbsRootVolumeSize=20
        )
    print(response)
    return response["JobFlowId"]