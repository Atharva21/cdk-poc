# A AWS CDK Template.

![workflow status](https://github.com/Atharva21/cdk-poc/actions/workflows/ci.yml/badge.svg)

A specially crafted AWS CDK template that is designed as a reference for a fully serverless application <br>
Simple, clean, and easy to get started with your custom requirements.

## Is it for you?

- Designed for beginners to quickly get started with AWS CDK.
- Uses python for the lambda backend and typescript for 'infrastructure as a code'.
- Stuck how to integrate AWS services with CDK? Or how to setup a python lambda testing pipeline? This template is for you to refer!

## Example architecture:

![cdk-poc](https://user-images.githubusercontent.com/35420813/153103540-c649c65d-dd72-4f0e-ba2f-62ca8aa4bb6d.jpg)

## Setup

- Clone repo `git clone https://github.com/Atharva21/cdk-poc.git`

- Setup python virtual environment `pipenv install`
  dont have pipenv? checkout [pipenv installation guide.](https://pipenv.pypa.io/en/latest/)

- Run python unit tests `pipenv run python -m pytest ./src`

- **Deploy** using [github workflow](https://github.com/Atharva21/cdk-poc/actions) or checkout manual deployment steps given below.

## Manual Deployment

- Create a lambda layer with all python dependencies

  ```bash
  pipenv run pip freeze > requirements.txt
  mkdir python
  cd python/
  pip install -r ../requirements.txt -t ./
  cd ..
  zip -r python.zip python
  ```

  this will create a `python.zip` as lambda layer for your lambdas

- Locally deploy using aws cdk:

  prerquisite: configure aws credentials(`aws_access_key_id`, `aws_secret_access_key`) under ~/.aws/credentials

  ```bash
  cd ./deploy
  yarn
  yarn cdk bootstrap
  yarn cdk deploy
  ```

- To destroy the deployed stack
  ```bash
  yarn cdk destroy
  ```
