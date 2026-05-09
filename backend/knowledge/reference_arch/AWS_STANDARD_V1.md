# Enterprise Standard: Secure Cloud Landing Zone (V1.2)

## Overview
This document defines the mandatory security controls for any cloud-based architectural proposal delivered by our consultants.

## Mandatory Controls
1. **Network Isolation**: All database workloads must reside in private subnets with no public internet route.
2. **Identity**: Least-privileged IAM roles must be used for all compute resources.
3. **Audit**: CloudTrail (AWS) or Activity Logs (Azure) must be enabled and shipped to a centralized security account.
4. **Resiliency**: Multi-Availability Zone (Multi-AZ) deployment is the default for production workloads.

## Preferred Services
- **Compute**: AWS Lambda or ECS Fargate (Serverless preferred).
- **Storage**: Amazon S3 with mandatory bucket versioning and object lock.
- **Database**: Amazon Aurora (PostgreSQL compatible) with RDS Proxy.
