import { Duration, RemovalPolicy, Stack, StackProps } from "aws-cdk-lib";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as s3 from "aws-cdk-lib/aws-s3";
import { LambdaIntegration, RestApi } from "aws-cdk-lib/aws-apigateway";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Table } from "aws-cdk-lib/aws-dynamodb";
import { Construct } from "constructs";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import * as path from "path";
import { ServicePrincipal } from "aws-cdk-lib/aws-iam";

export class CdkPocStack extends Stack {
	private _publisherFunction: Function;
	private _subscriberFunction: Function;
	private _api: RestApi;
	private _table: Table;
	private _bucket: Bucket;

	constructor(scope: Construct, id: string, props?: StackProps) {
		super(scope, id, props);

		// s3 bucket.
		this._bucket = new s3.Bucket(this, "bucket", {
			bucketName: "cdk-poc-site-bucket",
			blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
			versioned: false,
			encryption: s3.BucketEncryption.UNENCRYPTED,
			removalPolicy: RemovalPolicy.DESTROY,
			autoDeleteObjects: true,
		});

		// dynamoDB
		this._table = new dynamodb.Table(this, "table", {
			partitionKey: {
				name: "siteId",
				type: dynamodb.AttributeType.STRING,
			},
			sortKey: {
				name: "barcode",
				type: dynamodb.AttributeType.STRING,
			},
			tableName: "cdk-poc-site-table",
			removalPolicy: RemovalPolicy.DESTROY,
		});

		// rest api.
		this._api = new RestApi(this, "cdk-poc-api", {
			restApiName: "cdk-poc-api",
			description: "rest api to store site data in dynamo db.",
		});

		// lambda #1
		this._publisherFunction = new Function(this, "PublisherFunction", {
			runtime: Runtime.PYTHON_3_9,
			functionName: "publisher-function",
			code: Code.fromAsset(
				path.join(
					__dirname,
					"..",
					"src",
					"functions",
					"PublisherFunction"
				)
			),
			handler: "app.main",
			environment: {
				BUCKET_NAME: this._bucket.bucketName,
			},
		});

		// lambda #2
		this._subscriberFunction = new Function(this, "SubscriberFunction", {
			runtime: Runtime.PYTHON_3_9,
			functionName: "subscriber-function",
			code: Code.fromAsset(
				path.join(
					__dirname,
					"..",
					"src",
					"functions",
					"SubscriberFunction"
				)
			),
			handler: "app.main",
			environment: {
				BUCKET_NAME: this._bucket.bucketName,
			},
		});

		// setup post call to root to publisherLambda.
		const postSiteIntegration = new LambdaIntegration(
			this._publisherFunction,
			{
				timeout: Duration.seconds(29),
			}
		);
		this._api.root.addMethod("POST", postSiteIntegration);
	}
}
