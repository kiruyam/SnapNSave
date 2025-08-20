# SnapNSave
Secure receipt management app

SnapNSave is a **serverless web application** built using AWS services for secure, scalable receipt/bill data management. It allows users to upload images of receipts, automatically extracts relevant data using OCR, and stores it securely for later retrieval.

## Key Features

- Serverless architecture using AWS Lambda and API Gateway  
- OCR-based data extraction with Amazon Textract  
- Secure file storage in Amazon S3  
- Authentication via AWS Cognito  
- NoSQL database (Amazon DynamoDB) with KMS encryption  
- Scalable and cost-effective infrastructure with minimal maintenance  

---

## Technologies Used

- **AWS Cognito** – Authentication  
- **Amazon S3** – File Storage  
- **AWS Lambda** – Serverless Compute  
- **Amazon Textract** – OCR Processing  
- **Amazon DynamoDB** – NoSQL Database  
- **Amazon API Gateway** – REST API  

---

## System Flow

1. User logs in via AWS Cognito (frontend handled separately).  
2. Authenticated user uploads bill image to Amazon S3.  
3. S3 triggers `snapnsave-processbill` Lambda function.  
4. Lambda extracts key data (vendor, date, total) using Textract.  
5. Data is stored in DynamoDB with `userId` and `billId` as keys.  
6. User sends request to API Gateway (`GET /bills`).  
7. API Gateway triggers `snapnsave-fetchbills` Lambda to fetch data from DynamoDB.  

---

## AWS Resources

| Resource Name              | Purpose                                 |
|---------------------------|-----------------------------------------|
| `snapnsave-bills-storage` | S3 bucket for uploaded bill images      |
| `snapnsave-processbill`   | Lambda function to process uploads      |
| `snapnsave-fetchbills`    | Lambda function to fetch bill data      |
| `BillsTable`              | DynamoDB table for extracted bill info  |
| `GET /bills`              | API Gateway endpoint to retrieve bills  |
| Cognito User Pool         | User authentication                     |
| Cognito Identity Pool     | IAM role assignment for authenticated users |


