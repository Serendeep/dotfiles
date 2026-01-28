---
description: Generate API documentation and OpenAPI specs
argument-hint: "[path-to-api] [--openapi|--markdown|--postman]"
allowed-tools: Read, Write, Glob, Grep, Task
---

# API Documentation Generator

Generate comprehensive API documentation from code.

**Arguments**: "$ARGUMENTS"

## Output Formats

### --openapi (default)
Generate OpenAPI 3.0 specification (YAML)

### --markdown
Generate markdown documentation

### --postman
Generate Postman collection

## Workflow

1. **Analyze API Code**
   - Find route definitions
   - Extract handlers/controllers
   - Identify request/response schemas

2. **Launch API Documenter**
   Use Task tool to spawn `api-documenter` agent with:
   - API structure found
   - Output format requested

3. **Generate Documentation**
   - Endpoint definitions
   - Request/response schemas
   - Authentication requirements
   - Usage examples

4. **Output**
   Write to specified file or display

## Supported Frameworks

- Express.js / Fastify
- FastAPI / Flask / Django
- Spring Boot
- Go (Gin, Echo)
- NestJS

## Example Output

OpenAPI spec with:
- All endpoints documented
- Schema definitions
- Security schemes
- Example requests/responses
