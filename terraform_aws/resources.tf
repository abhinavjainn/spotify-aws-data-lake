## Lambda function

# IAM role for lambda function
resource "aws_iam_role" "lambda_execution_role" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# Lambda function
resource "aws_lambda_function" "spotify_data_lake" {
  filename      = "../lambda_package.zip"
  function_name = "spotify_data_lake"
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "app.lambda_handler"
  timeout       = "120"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = filebase64sha256("../lambda_package.zip")

  runtime = "python3.7"

  environment {
    variables = {
      SPOTIPY_CLIENT_ID = var.TF_VAR_SPOTIPY_CLIENT_ID,
      SPOTIPY_CLIENT_SECRET = var.TF_VAR_SPOTIPY_CLIENT_SECRET
    }
  }
}

# Lambda execution policy document
data "aws_iam_policy_document" "lambda_execution_policy_document" {
  statement {
    sid = "ManageLambdaFunction"
    effect = "Allow"
    actions = [
      "lambda:*",
      "ec2:*",
      "cloudwatch:*",
      "logs:*",
      "s3:*"
    ]
    resources = ["*"]
  }
}

# Lambda execution policy based on the policy document
resource "aws_iam_policy" "lambda_execution_policy" {
  name = "lambda_execution_policy"
  policy = data.aws_iam_policy_document.lambda_execution_policy_document.json
}

# Attach role to the policy
resource "aws_iam_role_policy_attachment" "lambda_execution_attachment" {
  role = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_execution_policy.arn
}

## Cloudwatch rules to trigger lambda function
# IAM
resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.spotify_data_lake.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.daily_spotify_lambda.arn
}

resource "aws_cloudwatch_event_rule" "daily_spotify_lambda" {
  name = "daily_spotify_lambda"
  description = "Trigger lambda daily"
  schedule_expression = "rate(1 day)"
  is_enabled = false
}

# Trigger
resource "aws_cloudwatch_event_target" "trigger_lambda" {
  rule = aws_cloudwatch_event_rule.daily_spotify_lambda.name
  target_id = "spotify_analysis"
  arn = aws_lambda_function.spotify_data_lake.arn
}