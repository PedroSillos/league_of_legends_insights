output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.lol_insights_data.bucket
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.mcp_server.function_name
}

output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = "${aws_api_gateway_rest_api.mcp_api.execution_arn}/prod/mcp"
}

output "api_gateway_invoke_url" {
  description = "Invoke URL of the API Gateway"
  value       = "https://${aws_api_gateway_rest_api.mcp_api.id}.execute-api.${var.aws_region}.amazonaws.com/prod/mcp"
}