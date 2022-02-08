# A AWS CDK Template.

A specially crafted AWS CDK template that is designed as a reference for a fully serverless application <br>
Simple, clean, and easy to get started with your custom requirements.

## Is it for you?
- Designed for beginners to quickly get started with AWS CDK.
- Uses python for the lambda backend and typescript for 'infrastructure as a code'.
- Stuck how to integrate AWS services with CDK? Or how to setup a python lambda testing pipeline? This template is for you to refer!  

## Architecture: 
![architecture](https://user-images.githubusercontent.com/35309821/153059229-0b156d4b-d8df-418e-a0ff-7d63fb940443.png)


## Deploy:
-   `npm run watch` watch for changes and compile
-   `npm run build` compile typescript to js
-   `npm run test` perform the jest unit tests
-   `cdk diff` compare deployed stack with current state
-   `cdk synth` emits the synthesized CloudFormation template
-   `cdk deploy` deploy this stack to your default AWS account/region

## Test lambda -> TODO:
