# A AWS CDK Template.

A specially crafted AWS CDK template that is designed as a reference for a fully serverless application <br>
Simple, clean, and easy to get started with your custom requirements.

## Is it for you?
- Designed for beginners to quickly get started with AWS CDK.
- Uses python for the lambda backend and typescript for 'infrastructure as a code'.
- Stuck how to integrate AWS services with CDK? Or how to setup a python lambda testing pipeline? This template is for you to refer!  

## Architecture: 
![cdk-poc](https://user-images.githubusercontent.com/35420813/153103540-c649c65d-dd72-4f0e-ba2f-62ca8aa4bb6d.jpg)

## Deploy:
-   `npm run watch` watch for changes and compile
-   `npm run build` compile typescript to js
-   `npm run test` perform the jest unit tests
-   `cdk diff` compare deployed stack with current state
-   `cdk synth` emits the synthesized CloudFormation template
-   `cdk deploy` deploy this stack to your default AWS account/region

## Test lambda -> TODO:
