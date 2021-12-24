import {
	aws_lambda_event_sources,
	Duration,
	RemovalPolicy,
	Stack,
	StackProps,
} from "aws-cdk-lib";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as s3 from "aws-cdk-lib/aws-s3";
import { LambdaIntegration, RestApi } from "aws-cdk-lib/aws-apigateway";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Table } from "aws-cdk-lib/aws-dynamodb";
import { Construct } from "constructs";
import { Code, Function, LayerVersion, Runtime } from "aws-cdk-lib/aws-lambda";
import * as path from "path";
import { Queue } from "aws-cdk-lib/aws-sqs";

export class CdkPocStack extends Stack {
	private _publisherFunction: Function;
	private _subscriberFunction: Function;
	private _lambdaLayer: LayerVersion;
	private _api: RestApi;
	private _table: Table;
	private _bucket: Bucket;
	private _sqs: Queue;

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
			deployOptions: {
				stageName: "beta",
			},
		});

		//sqs.
		this._sqs = new Queue(this, "queue", {
			queueName: "cdk-poc-site-queue",
			removalPolicy: RemovalPolicy.DESTROY,
		});

		// the lambda layer
		this._lambdaLayer = new LayerVersion(this, "cdk-poc-python-layer", {
			code: Code.fromAsset(
				path.join(__dirname, "..", "..", "python.zip")
			),
			compatibleRuntimes: [Runtime.PYTHON_3_8, Runtime.PYTHON_3_9],
			description: "python lambda layer with third party libraries",
		});

		// lambda #1
		this._publisherFunction = new Function(this, "PublisherFunction", {
			runtime: Runtime.PYTHON_3_9,
			functionName: "publisher-function",
			code: Code.fromAsset(
				path.join(
					__dirname,
					"..",
					"..",
					"src",
					"functions",
					"PublisherFunction"
				)
			),
			handler: "app.main",
			environment: {
				BUCKET_NAME: this._bucket.bucketName,
				QUEUE_NAME: this._sqs.queueName,
			},
			layers: [this._lambdaLayer],
		});

		// lambda #2
		this._subscriberFunction = new Function(this, "SubscriberFunction", {
			runtime: Runtime.PYTHON_3_9,
			functionName: "subscriber-function",
			code: Code.fromAsset(
				path.join(
					__dirname,
					"..",
					"..",
					"src",
					"functions",
					"SubscriberFunction"
				)
			),
			handler: "app.main",
			environment: {
				BUCKET_NAME: this._bucket.bucketName,
				TABLE_NAME: this._table.tableName,
			},
			layers: [this._lambdaLayer],
		});

		// setup post call to root to publisherLambda.
		const postSiteIntegration = new LambdaIntegration(
			this._publisherFunction,
			{
				timeout: Duration.seconds(29),
			}
		);
		this._api.root.addMethod("POST", postSiteIntegration);

		// sqs access and subscriber trigger.
		this._sqs.grantSendMessages(this._publisherFunction);
		this._sqs.grantConsumeMessages(this._subscriberFunction);
		const eventSource = new aws_lambda_event_sources.SqsEventSource(
			this._sqs
		);
		this._subscriberFunction.addEventSource(eventSource);

		// table access.
		this._table.grantWriteData(this._subscriberFunction);

		// s3 access.
		this._bucket.grantWrite(this._publisherFunction);
		this._bucket.grantRead(this._subscriberFunction);
		this._bucket.grantDelete(this._subscriberFunction);
	}
}
