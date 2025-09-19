#!/bin/bash

echo "🚀 Deploying League of Legends Insights to AWS..."

# Create deployment package
echo "📦 Creating Lambda deployment package..."
cd ..
zip -r infrastructure/mcp_server.zip *.py -x "tests/*" "infrastructure/*" "*.pyc" "__pycache__/*"
cd infrastructure

# Initialize Terraform
echo "🔧 Initializing Terraform..."
terraform init

# Plan deployment
echo "📋 Planning deployment..."
terraform plan

# Apply deployment
echo "✅ Applying deployment..."
terraform apply -auto-approve

# Get outputs
echo "📊 Deployment complete! Outputs:"
terraform output

echo "🎉 Deployment finished successfully!"