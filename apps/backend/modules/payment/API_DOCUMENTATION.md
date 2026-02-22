# Payment Module API Documentation

## Overview

Complete Payment API for the SILA System with support for:

- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Payment transactions
- ✅ Refunds and partial refunds
- ✅ Webhooks and event notifications
- ✅ Audit logging
- ✅ Receipt generation (PDF, HTML, JSON)
- ✅ Statistics and analytics
- ✅ JWT security
- ✅ Advanced validation
- ✅ Rate limiting

## Base URL

```
/api/v1/payment
```

## Authentication

All endpoints (except `/ping` and `/status`) require JWT token in the `Authorization`
header:

```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Health Check

#### GET `/ping`

Health check endpoint.

**Response:**

```json
{
  "status": "payment ok",
  "timestamp": "2024-12-09T16:43:00.000000",
  "service": "payment-module"
}
```

#### GET `/status`

Detailed status with all available endpoints.

**Response:**

```json
{
  "status": "healthy",
  "service": "payment",
  "version": "1.0.0",
  "timestamp": "2024-12-09T16:43:00.000000",
  "endpoints": { ... }
}
```

---

### Payment CRUD Operations

#### POST `/`

Create a new payment.

**Request Body:**

```json
{
  "amount": 1000.0,
  "currency": "AOA",
  "method": "bna",
  "description": "Service payment",
  "reference": "REF-12345",
  "metadata_": {
    "service_id": 123,
    "client_id": 456
  }
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "amount": 1000.00,
  "currency": "AOA",
  "status": "pending",
  "method": "bna",
  "reference": "REF-12345",
  "description": "Service payment",
  "metadata_": { ... },
  "created_at": "2024-12-09T16:43:00.000000",
  "updated_at": "2024-12-09T16:43:00.000000"
}
```

#### GET `/`

List all payments with filters.

**Query Parameters:**

- `status` (optional): Filter by status (pending, processing, completed, failed,
  refunded, etc.)
- `method` (optional): Filter by payment method
- `date_from` (optional): Filter from date (YYYY-MM-DD)
- `date_to` (optional): Filter to date (YYYY-MM-DD)
- `min_amount` (optional): Minimum amount
- `max_amount` (optional): Maximum amount
- `skip` (optional, default: 0): Number of records to skip
- `limit` (optional, default: 100, max: 1000): Number of records to return

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "amount": 1000.00,
    "currency": "AOA",
    "status": "completed",
    "method": "bna",
    "reference": "REF-12345",
    ...
  }
]
```

#### GET `/{payment_id}`

Get a specific payment by ID.

**Response:** `200 OK`

```json
{
  "id": 1,
  "amount": 1000.00,
  ...
}
```

#### GET `/reference/{reference}`

Get a payment by reference.

**Response:** `200 OK`

#### PUT `/{payment_id}`

Update a payment.

**Request Body:**

```json
{
  "status": "processing",
  "description": "Updated description",
  "metadata_": { ... }
}
```

**Response:** `200 OK`

#### DELETE `/{payment_id}`

Delete a payment (only pending or failed payments).

**Response:** `204 No Content`

---

### Transactions

#### POST `/{payment_id}/transaction`

Create a transaction for a payment.

**Query Parameters:**

- `transaction_type` (required): Type of transaction (payment, refund, adjustment, fee)
- `amount` (optional): Transaction amount (defaults to payment amount)

**Response:** `201 Created`

```json
{
  "id": 1,
  "payment_id": 1,
  "amount": 1000.0,
  "currency": "AOA",
  "type": "payment",
  "status": "pending",
  "reference": "TXN-ABC123",
  "provider_reference": null,
  "created_at": "2024-12-09T16:43:00.000000"
}
```

#### GET `/transaction/{transaction_id}`

Get a specific transaction.

**Response:** `200 OK`

#### GET `/{payment_id}/transactions`

List all transactions for a payment.

**Query Parameters:**

- `skip` (optional, default: 0)
- `limit` (optional, default: 100)

**Response:** `200 OK`

---

### Refunds

#### POST `/{payment_id}/refund`

Create a refund for a payment.

**Request Body:**

```json
{
  "amount": 500.00,
  "reason": "Partial refund",
  "metadata_": { ... }
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "payment_id": 1,
  "amount": 500.0,
  "currency": "AOA",
  "status": "pending",
  "reference": "RFD-XYZ789",
  "created_at": "2024-12-09T16:43:00.000000"
}
```

#### GET `/refund/{refund_id}`

Get a specific refund.

**Response:** `200 OK`

#### GET `/{payment_id}/refunds`

List all refunds for a payment.

**Query Parameters:**

- `skip` (optional, default: 0)
- `limit` (optional, default: 100)

**Response:** `200 OK`

---

### Statistics & Analytics

#### GET `/statistics`

Get overall payment statistics.

**Response:** `200 OK`

```json
{
  "timestamp": "2024-12-09T16:43:00.000000",
  "statistics": {
    "total_payments": 150,
    "total_amount": 50000.0,
    "completed_payments": 120,
    "completed_amount": 45000.0,
    "pending_payments": 30
  }
}
```

#### GET `/{payment_id}/summary`

Get complete summary of a payment with transactions and refunds.

**Response:** `200 OK`

```json
{
  "payment": { ... },
  "transactions": [ ... ],
  "refunds": [ ... ],
  "summary": {
    "total_transactions": 2,
    "total_refunds": 1,
    "refunded_amount": 500.00,
    "remaining_amount": 500.00
  }
}
```

---

### Audit Log

#### GET `/audit-log`

Get audit log of payment operations.

**Query Parameters:**

- `payment_id` (optional): Filter by payment ID
- `action` (optional): Filter by action (create, update, refund, etc.)
- `skip` (optional, default: 0)
- `limit` (optional, default: 100)

**Response:** `200 OK`

```json
{
  "total": 5,
  "logs": [
    {
      "id": 1,
      "payment_id": 1,
      "action": "create",
      "user_id": 123,
      "details": { ... },
      "created_at": "2024-12-09T16:43:00.000000"
    }
  ]
}
```

---

### Webhooks

#### POST `/webhook/register`

Register a webhook for payment events.

**Query Parameters:**

- `url` (required): Webhook URL
- `events` (required): List of events to trigger webhook

**Available Events:**

- `payment.created`
- `payment.completed`
- `payment.failed`
- `payment.refunded`
- `transaction.created`
- `transaction.completed`

**Response:** `200 OK`

```json
{
  "id": 1,
  "url": "https://example.com/webhook",
  "events": ["payment.created", "payment.completed"],
  "active": true,
  "created_at": "2024-12-09T16:43:00.000000"
}
```

#### POST `/webhook/test`

Test a webhook by sending a test event.

**Query Parameters:**

- `webhook_id` (required): Webhook ID to test

**Response:** `200 OK`

```json
{
  "status": "test_sent",
  "webhook_id": 1,
  "timestamp": "2024-12-09T16:43:00.000000"
}
```

---

### Receipts

#### GET `/{payment_id}/receipt`

Get receipt for a payment.

**Query Parameters:**

- `format` (optional, default: "pdf"): Receipt format (pdf, json, html)

**Response:**

- `pdf`: Binary PDF file
- `json`: JSON object with receipt data
- `html`: HTML string

---

## Payment Methods

Supported payment methods:

- `bna` - BNA (Banco Nacional de Angola)
- `unitel_money` - Unitel Money
- `m_pesa` - M-Pesa
- `multicaixa` - Multicaixa
- `credit_card` - Credit Card
- `bank_transfer` - Bank Transfer
- `cash` - Cash

---

## Payment Status

- `pending` - Payment created, awaiting processing
- `processing` - Payment is being processed
- `completed` - Payment successfully completed
- `failed` - Payment failed
- `refunded` - Payment fully refunded
- `partially_refunded` - Payment partially refunded
- `cancelled` - Payment cancelled

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

---

## Rate Limiting

- **Limit:** 100 requests per minute
- **Identifier:** User ID or IP address
- **Headers:** `X-RateLimit-Remaining` shows remaining requests

---

## Security

1. **JWT Authentication:** All endpoints require valid JWT token
2. **Input Validation:** All inputs are validated
3. **Rate Limiting:** Prevents abuse
4. **Audit Logging:** All operations are logged
5. **HTTPS:** Use HTTPS in production

---

## Examples

### Create a Payment

```bash
curl -X POST http://localhost:8000/api/v1/payment/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1000.00,
    "currency": "AOA",
    "method": "bna",
    "description": "Service payment"
  }'
```

### List Payments

```bash
curl -X GET "http://localhost:8000/api/v1/payment/?status=completed&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Create a Refund

```bash
curl -X POST http://localhost:8000/api/v1/payment/1/refund \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 500.00,
    "reason": "Partial refund"
  }'
```

### Get Receipt

```bash
curl -X GET "http://localhost:8000/api/v1/payment/1/receipt?format=pdf" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -o receipt.pdf
```

---

## Support

For issues or questions, contact the development team.
