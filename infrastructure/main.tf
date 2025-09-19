terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 bucket for data storage
resource "aws_s3_bucket" "lol_insights_data" {
  bucket = "${var.project_name}-data-${random_string.suffix.result}"
}

resource "aws_s3_bucket_versioning" "lol_insights_data_versioning" {
  bucket = aws_s3_bucket.lol_insights_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Lambda function for MCP server
resource "aws_lambda_function" "mcp_server" {
  filename         = "mcp_server.zip"
  function_name    = "${var.project_name}-mcp-server"
  role            = aws_iam_role.lambda_role.arn
  handler         = "mcp_server.lambda_handler"
  runtime         = "python3.9"
  timeout         = 300

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.lol_insights_data.bucket
    }
  }
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.lol_insights_data.arn}/*"
      }
    ]
  })
}

# API Gateway for MCP server
resource "aws_api_gateway_rest_api" "mcp_api" {
  name = "${var.project_name}-mcp-api"
}

resource "aws_api_gateway_resource" "mcp_resource" {
  rest_api_id = aws_api_gateway_rest_api.mcp_api.id
  parent_id   = aws_api_gateway_rest_api.mcp_api.root_resource_id
  path_part   = "mcp"
}

resource "aws_api_gateway_method" "mcp_method" {
  rest_api_id   = aws_api_gateway_rest_api.mcp_api.id
  resource_id   = aws_api_gateway_resource.mcp_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "mcp_integration" {
  rest_api_id = aws_api_gateway_rest_api.mcp_api.id
  resource_id = aws_api_gateway_resource.mcp_resource.id
  http_method = aws_api_gateway_method.mcp_method.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.mcp_server.invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.mcp_server.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.mcp_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "mcp_deployment" {
  depends_on = [
    aws_api_gateway_method.mcp_method,
    aws_api_gateway_integration.mcp_integration,
  ]

  rest_api_id = aws_api_gateway_rest_api.mcp_api.id
  stage_name  = "prod"
}