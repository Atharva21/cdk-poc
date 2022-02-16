# An AWS CDK Template.

![workflow status](https://github.com/Atharva21/cdk-poc/actions/workflows/ci.yml/badge.svg) [![codecov](https://codecov.io/gh/Atharva21/cdk-poc/branch/main/graph/badge.svg)](https://codecov.io/gh/Atharva21/cdk-poc)

A specially crafted AWS CDK template that is designed as a reference for a fully serverless application <br>
Simple, clean, and easy to get started with your custom requirements.

## Is it for you?

- Designed for beginners to quickly get started with AWS CDK.
- Uses python for the lambda backend and typescript for 'infrastructure as a code'.
- Stuck how to integrate AWS services with CDK? Or how to setup a python lambda testing and deployment pipeline? This template is for you to refer!

## Setup

- **Fork repo** & clone

  ```bash
  git clone https://github.com/<USERNAME>/cdk-poc.git
  cd ./cdk-poc
  ```

- Setup python virtual environment

  ```bash
  pipenv install --dev
  ```

  dont have pipenv? checkout [pipenv installation guide.](https://pipenv.pypa.io/en/latest/)

- **Develop**:

  - For changes in **AWS deploy stack**, navigate to `deploy`
    ```bash
    cd ./deploy/
    ```
    install npm packages
    ```bash
    yarn
    ```
    You can edit the template stack in `deploy/lib/cdk-poc-stack.ts`.
    In this file, we can create infrastructure as code, for reference check out [AWS CDK documentation](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib-readme.html)
    - ##### Example template architecture:
      You will find below stack in the template you can add/delete components as per your needs.<br>
      ![cdk-poc](https://user-images.githubusercontent.com/35420813/153103540-c649c65d-dd72-4f0e-ba2f-62ca8aa4bb6d.jpg)
  - For changes in **Lambda** functions, navigate to `src/functions`
    ```bash
    cd ./src/functions/
    ```
    Here you will find two template functions `Producer` and `Consumer`
    You can edit/add/delete your own lambda functions here, just _ensure that they are referred in the stack file mentioned above_
    Note that lambda layer creation is taken care in [CI workflow](https://github.com/Atharva21/cdk-poc/blob/b66804d2970aba01eebaa8c740fda4e8bb8b6363/.github/workflows/ci.yml#L66) so you need not worry about it.

- **Test**:

  - Template uses pytest with moto to mock aws environment
    to run the tests
    ```bash
    pipenv run python -m pytest ./src/tests/
    ```
  - To generate a coverage report

    ```bash
    pipenv run python -m pytest ./src/tests/ --cov=. --cov-report=html
    ```

  - Run Linter
    ```bash
    pipenv run python -m flake8 ./src
    ```

- **Deploy:**
  In order to use the CI workflow we need these three github repo secrets

  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`

  checkout how to [find access & secret keys](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)

  once these are configured, we can simply **push / merge** on the main branch which will trigger a [CI workflow](https://github.com/Atharva21/cdk-poc/actions/workflows/ci.yml) to **build, test and deploy stack on aws**.
  The workflow will generate a artifact named `aws-artifacts` which can be downloaded post workflow run.

  For **pull requests**, CI workflow will only build and test, and **not** deploy.

- **Destroy:**
  In order to destroy/takedown the deployed stack in your AWS account, you can manually run the [teardown workflow](https://github.com/Atharva21/cdk-poc/actions/workflows/teardown.yml).
  It destroys all the resources created under the `cdk-stack` file.

<!-- CONTRIBUTING -->

### Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.
