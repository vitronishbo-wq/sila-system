# Commercial Module (Sistema Comercial)

# SILA System - Backend

## 📋 Description

The Commercial module is responsible for complete management of the commercial system in
SILA, including business licensing, registration of commercial activities, and
integration with regulatory bodies. It implements essential functionalities for
formalization and monitoring of municipal business activities.

## 🚀 Core Functionalities

- 🏢 **Business Licensing** - Complete process for obtaining permits and licenses
- 📊 **Activity Registration** - Registration and classification of businesses
- 🔄 **License Management** - Control of validity and automatic renewal
- 🔗 **Regulatory Integration** - Connection with health surveillance systems
- 📈 **Commercial Reports** - Metrics and economic indicators
- 🏪 **Business Portal** - Self-service area for business owners
- 📋 **Economic Activity Catalog** - Classification and categorization system
- 🔍 **Business Intelligence** - Analytics and commercial insights

## 📡 Available Endpoints

| Method | Endpoint                          | Description                        | Authentication | Rate Limit | Status     |
| ------ | --------------------------------- | ---------------------------------- | -------------- | ---------- | ---------- |
| `GET`  | `/commercial/ping`                | Module health check                | ❌ Public      | 100/hour   | ✅ Active  |
| `GET`  | `/commercial/services`            | List available commercial services | ✅ Required    | 1000/hour  | 🚧 Planned |
| `POST` | `/commercial/licenses`            | Request commercial license         | ✅ Required    | 100/hour   | 🚧 Planned |
| `GET`  | `/commercial/licenses`            | User's licenses                    | ✅ Required    | 500/hour   | 🚧 Planned |
| `GET`  | `/commercial/licenses/{id}`       | Specific license details           | ✅ Required    | 500/hour   | 🚧 Planned |
| `PUT`  | `/commercial/licenses/{id}/renew` | Renew commercial license           | ✅ Required    | 50/hour    | 🚧 Planned |
| `GET`  | `/commercial/activities`          | List economic activities           | ✅ Required    | 1000/hour  | 🚧 Planned |
| `POST` | `/commercial/activities`          | Register new economic activity     | ✅ Required    | 100/hour   | 🚧 Planned |

### ⚠️ Current Status - Basic Development Phase

**Note:** Module is in initial implementation phase with only health check endpoint
active.

## 🔧 Configuration

### Technology Stack

- **Framework:** FastAPI with organized modular structure
- **Database:** PostgreSQL with SQLAlchemy models (12 models)
- **Authentication:** JWT required for business endpoints
- **Architecture:** Complete MVC with services, routes, and schemas
- **Validation:** 11 Pydantic schemas for data validation
- **Testing:** Basic coverage implemented

### Environment Variables

```bash
# Commercial Module Configuration
COMMERCIAL_DB_URL=postgresql://user:pass@localhost/sila_commercial
COMMERCIAL_JWT_SECRET_KEY=your-secret-key
COMMERCIAL_JWT_ALGORITHM=HS256
# 90 dias em minutos (90 * 24 * 60 = 129600)
COMMERCIAL_ACCESS_TOKEN_EXPIRE_MINUTES=129600

# External Integrations
COMMERCIAL_REGULATOR_API_URL=https://api.regulator.gov.ao
COMMERCIAL_REGULATOR_API_KEY=regulator-api-key
COMMERCIAL_SANITARY_SURVEILLANCE_URL=https://surveillance.gov.ao

# Business Rules
COMMERCIAL_LICENSE_VALIDITY_DAYS=365
COMMERCIAL_RENEWAL_REMINDER_DAYS=30
COMMERCIAL_MAX_LICENSES_PER_BUSINESS=10

# File Storage
COMMERCIAL_DOCUMENTS_BUCKET=sila-commercial-docs
COMMERCIAL_MAX_DOCUMENT_SIZE=10485760  # 10MB
```

## 🗂️ Module Structure

```
commercial/
├── __init__.py          # Initialization and configuration (639 lines)
├── endpoints.py         # API route definitions (7 lines - basic)
├── models/              # SQLAlchemy models (12 files)
│   ├── __init__.py
│   ├── business.py      # Business entity model
│   ├── license.py       # Commercial license model
│   ├── activity.py      # Economic activity model
│   ├── permit.py        # Business permit model
│   ├── inspection.py    # Inspection record model
│   ├── renewal.py       # License renewal model
│   ├── document.py      # Business document model
│   ├── category.py      # Business category model
│   ├── fee.py           # License fee model
│   ├── violation.py     # Commercial violation model
│   ├── audit.py         # Commercial audit model
│   └── notification.py  # Business notification model
├── schemas/             # Pydantic schemas (11 files)
│   ├── __init__.py
│   ├── business.py      # Business validation schemas
│   ├── license.py       # License validation schemas
│   ├── activity.py      # Activity validation schemas
│   ├── permit.py        # Permit validation schemas
│   ├── inspection.py    # Inspection validation schemas
│   ├── renewal.py       # Renewal validation schemas
│   ├── document.py      # Document validation schemas
│   ├── category.py      # Category validation schemas
│   ├── fee.py           # Fee validation schemas
│   └── violation.py     # Violation validation schemas
├── services/            # Business logic (1 file)
│   ├── __init__.py
│   └── commercial_service.py  # Core commercial operations
├── routes/              # Organized routes (12 files)
│   ├── __init__.py
│   ├── business.py      # Business management routes
│   ├── license.py       # License management routes
│   ├── activity.py      # Activity management routes
│   ├── permit.py        # Permit management routes
│   ├── inspection.py    # Inspection routes
│   ├── renewal.py       # Renewal routes
│   ├── document.py      # Document routes
│   ├── category.py      # Category routes
│   ├── fee.py           # Fee routes
│   ├── violation.py     # Violation routes
│   └── notification.py  # Notification routes
├── tests/               # Automated tests (1 file)
│   ├── __init__.py
│   └── test_commercial.py  # Commercial module tests
└── README.md            # This documentation
```

## 📚 Usage Examples

### FastAPI Integration Example

```python
from fastapi import FastAPI, Depends
from app.modules.commercial import router
from app.core.auth import get_current_user

app = FastAPI(title="SILA Commercial API")
app.include_router(router, prefix="/commercial", tags=["commercial"])

@app.get("/commercial/health")
async def health_check():
    return {"status": "healthy", "module": "commercial"}

# Protected endpoint example
@app.get("/commercial/dashboard")
async def commercial_dashboard(current_user = Depends(get_current_user)):
    return {"user": current_user.email, "licenses": await get_user_licenses(current_user.id)}
```

### Complete HTTP Client Example

```bash
# Health check (public)
curl -X GET "http://localhost:8000/commercial/ping" \
  -H "Accept: application/json"

# Get authentication token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "business@example.com",
    "password": "secure_password"
  }'

# Get commercial services (authenticated)
curl -X GET "http://localhost:8000/commercial/services" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Request commercial license (authenticated)
curl -X POST "http://localhost:8000/commercial/licenses" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "businessName": "Empresa Exemplo Ltda",
    "businessType": "Comércio Varejista",
    "cnaeCode": "4751201",
    "address": {
      "street": "Rua das Flores",
      "number": "123",
      "city": "Luanda",
      "province": "Luanda",
      "postalCode": "12345-678"
    },
    "contactInfo": {
      "phone": "+244 923 456 789",
      "email": "contato@empresa.com"
    },
    "activities": [
      {
        "code": "4751201",
        "description": "Comércio varejista de artigos de vestuário e acessórios"
      }
    ]
  }'

# Get user licenses (authenticated)
curl -X GET "http://localhost:8000/commercial/licenses" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Get specific license details (authenticated)
curl -X GET "http://localhost:8000/commercial/licenses/123" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Renew license (authenticated)
curl -X PUT "http://localhost:8000/commercial/licenses/123/renew" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "renewalPeriod": 365,
    "paymentMethod": "credit_card"
  }'
```

### Frontend Integration Example

```typescript
// commercial-api.ts
import { apiClient } from '@/lib/api-client';

export interface CommercialLicense {
  id: string;
  businessName: string;
  licenseNumber: string;
  status: 'active' | 'expired' | 'pending' | 'suspended';
  validityPeriod: {
    start: Date;
    end: Date;
  };
  activities: Array<{
    code: string;
    description: string;
  }>;
}

export interface CommercialService {
  id: string;
  name: string;
  description: string;
  requirements: string[];
  fees: Array<{
    type: string;
    amount: number;
    currency: string;
  }>;
}

export const commercialAPI = {
  // Get available commercial services
  async getServices(): Promise<CommercialService[]> {
    const response = await apiClient.get('/commercial/services');
    return response.data;
  },

  // Get user's commercial licenses
  async getUserLicenses(): Promise<CommercialLicense[]> {
    const response = await apiClient.get('/commercial/licenses');
    return response.data;
  },

  // Get specific license details
  async getLicenseDetails(licenseId: string): Promise<CommercialLicense> {
    const response = await apiClient.get(`/commercial/licenses/${licenseId}`);
    return response.data;
  },

  // Request new commercial license
  async requestLicense(licenseData: any): Promise<CommercialLicense> {
    const response = await apiClient.post('/commercial/licenses', licenseData);
    return response.data;
  },

  // Renew existing license
  async renewLicense(licenseId: string, renewalData: any): Promise<CommercialLicense> {
    const response = await apiClient.put(`/commercial/licenses/${licenseId}/renew`, renewalData);
    return response.data;
  }
};

// React component example
import React, { useState, useEffect } from 'react';
import { commercialAPI, CommercialLicense } from '@/features/commercial/api';

export const CommercialDashboard: React.FC = () => {
  const [licenses, setLicenses] = useState<CommercialLicense[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadLicenses = async () => {
      try {
        const userLicenses = await commercialAPI.getUserLicenses();
        setLicenses(userLicenses);
      } catch (error) {
        console.error('Error loading commercial licenses:', error);
      } finally {
        setLoading(false);
      }
    };

    loadLicenses();
  }, []);

  if (loading) return <div>Loading commercial data...</div>;

  return (
    <div className="commercial-dashboard">
      <h2>Commercial Licenses</h2>
      {licenses.map(license => (
        <div key={license.id} className="license-card">
          <h3>{license.businessName}</h3>
          <p>License: {license.licenseNumber}</p>
          <p>Status: {license.status}</p>
          <p>Valid until: {license.validityPeriod.end.toLocaleDateString()}</p>
        </div>
      ))}
    </div>
  );
};
```

## 🔗 Dependencies

### Internal Dependencies

- **FastAPI** - Asynchronous web framework
- **SQLAlchemy** - ORM for commercial models
- **Pydantic** - Data validation for business information
- **Redis** - Caching and session management
- **Celery** - Background task processing
- **Boto3** - S3 integration for document storage

### Module Dependencies

- `app.core.auth` - Authentication system
- `app.db.session` - Database connection management
- `app.models.base` - Base system models
- `app.core.config` - Configuration management
- `app.core.security` - Security utilities
- `app.modules.notifications` - Notification system
- `app.modules.documents` - Document management
- `app.modules.payment` - Payment processing

### External Dependencies

- **Regulatory API** - Government licensing systems
- **Sanitary Surveillance** - Health inspection systems
- **Tax Authority API** - Business registration verification
- **Postal Service API** - Address validation
- **Banking API** - Payment processing
- **Email Service** - License notifications

## ⚠️ Important Observations

### Development Environment

- **Module in development** - Basic implementation in progress
- **Structure prepared** - 12 models and 11 schemas ready
- **Testing framework** - Basic test coverage implemented
- **API documentation** - OpenAPI/Swagger integration needed
- **Development data** - Mock data for testing required

### Production Environment

- **Sensitive business data** - Requires careful handling of commercial information
- **Regulatory compliance** - Must follow municipal and federal regulations
- **Integration required** - Connection with inspection systems
- **Performance optimization** - Index optimization for commercial queries
- **Backup strategy** - Regular backups of license data
- **Monitoring** - Real-time monitoring of license operations

### Security Considerations

- **Business data protection** - Encrypt sensitive commercial information
- **Access control** - Role-based permissions for license operations
- **Audit logging** - Complete audit trail for all commercial operations
- **Document security** - Secure storage and access to business documents
- **API rate limiting** - Prevent abuse of commercial endpoints
- **Data retention** - Compliance with data retention policies

### Performance Considerations

- **Query optimization** - Efficient queries for large commercial datasets
- **Caching strategy** - Redis for frequently accessed commercial data
- **Batch processing** - Handle bulk license operations efficiently
- **Database indexing** - Optimize indexes for commercial queries
- **Async processing** - Background tasks for heavy operations

## 🔒 Security Implementation

### Implemented Security Measures

- ✅ **JWT Authentication** - Token-based authentication for all endpoints
- ✅ **Input Validation** - Pydantic schemas for data validation
- ✅ **SQL Injection Protection** - SQLAlchemy ORM protection
- ✅ **CORS Configuration** - Cross-origin request security
- ✅ **Rate Limiting** - API endpoint protection
- ✅ **HTTPS Enforcement** - Secure communication

### Security Recommendations

- 🔒 **Business Data Encryption** - Encrypt sensitive commercial information
- 🔒 **Document Access Control** - Implement granular document permissions
- 🔒 **Audit Trail Enhancement** - Detailed logging of all commercial operations
- 🔒 **API Key Management** - Secure handling of external API keys
- 🔒 **Data Masking** - Mask sensitive data in logs and responses
- 🔒 **Regular Security Audits** - Periodic security assessments

## 📊 Analytics and Monitoring

### Key Performance Indicators (KPIs)

- **License Processing Time** - Average time for license approval
- **Business Registration Rate** - New businesses registered per month
- **License Renewal Rate** - Percentage of licenses renewed on time
- **API Response Time** - Average response time for commercial endpoints
- **Error Rate** - Percentage of failed commercial operations
- **User Satisfaction** - Feedback from business owners

### Monitoring Metrics

```python
# Commercial module metrics
COMMERCIAL_METRICS = {
    'licenses_processed': Counter('commercial_licenses_processed_total'),
    'licenses_approved': Counter('commercial_licenses_approved_total'),
    'licenses_rejected': Counter('commercial_licenses_rejected_total'),
    'renewals_processed': Counter('commercial_renewals_processed_total'),
    'api_requests': Counter('commercial_api_requests_total'),
    'api_response_time': Histogram('commercial_api_response_time_seconds'),
    'active_businesses': Gauge('commercial_active_businesses_total'),
    'pending_licenses': Gauge('commercial_pending_licenses_total'),
    'expired_licenses': Gauge('commercial_expired_licenses_total')
}
```

### Health Checks

```python
@app.get("/commercial/health")
async def health_check():
    checks = {
        "database": await check_database_connection(),
        "redis": await check_redis_connection(),
        "external_apis": await check_regulatory_apis(),
        "storage": await check_document_storage()
    }

    overall_status = "healthy" if all(checks.values()) else "unhealthy"

    return {
        "status": overall_status,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

### Alerts Configuration

```yaml
# Commercial module alerts
alerts:
  - name: "High License Processing Time"
    condition: "commercial_license_processing_time > 48h"
    severity: "warning"

  - name: "License Expiry Rate"
    condition: "commercial_expired_licenses_rate > 10%"
    severity: "critical"

  - name: "API Error Rate"
    condition: "commercial_api_error_rate > 5%"
    severity: "warning"

  - name: "Database Connection Issues"
    condition: "commercial_database_connection_failed"
    severity: "critical"
```

## 🔄 Workflow Diagrams

### License Application Workflow

```mermaid
flowchart TD
    A[Business Owner] --> B[Submit Application]
    B --> C[Document Validation]
    C --> D{Documents Valid?}
    D -->|No| E[Request Additional Documents]
    E --> C
    D -->|Yes| F[Business Verification]
    F --> G{Business Verified?}
    G -->|No| H[Reject Application]
    G -->|Yes| I[Regulatory Check]
    I --> J{Regulatory Approval?}
    J -->|No| K[Request Clarifications]
    K --> I
    J -->|Yes| L[Calculate Fees]
    L --> M[Payment Processing]
    M --> N{Payment Successful?}
    N -->|No| O[Payment Retry]
    O --> M
    N -->|Yes| P[Issue License]
    P --> Q[Send Notification]
    Q --> R[Active License]
```

### License Renewal Workflow

```mermaid
flowchart TD
    A[System Check] --> B{License Expiring Soon?}
    B -->|No| A
    B -->|Yes| C[Send Renewal Notice]
    C --> D[Business Owner Action]
    D --> E[Submit Renewal Request]
    E --> F[Validate Renewal Eligibility]
    F --> G{Eligible for Renewal?}
    G -->|No| H[Reject with Reason]
    G -->|Yes| I[Update Business Information]
    I --> J[Regulatory Compliance Check]
    J --> K{Compliant?}
    K -->|No| L[Require Compliance Actions]
    L --> M[Business Compliance]
    M --> J
    K -->|Yes| N[Calculate Renewal Fees]
    N --> O[Payment Processing]
    O --> P{Payment Successful?}
    P -->|No| Q[Payment Retry]
    Q --> O
    P -->|Yes| R[Issue Renewed License]
    R --> S[Update Records]
    S --> T[Send Confirmation]
```

## 👥 Responsibilities

### Development Team

- **Module Owner:** SILA Commercial Team
- **Lead Developer:** Commercial Module Lead
- **Backend Developers:** 2 developers
- **QA Engineer:** 1 tester
- **DevOps Engineer:** Infrastructure support

### Contact Information

- **Email:** dev@sila.gov.ao
- **Slack:** #sila-backend-commercial
- **Jira:** SILA-COMMERCIAL
- **Documentation:** https://docs.sila.gov.ao/commercial

### Support Hours

- **Development Support:** Monday - Friday, 9:00 - 18:00 (UTC+1)
- **Production Support:** 24/7 on-call rotation
- **Emergency Contact:** +244 923 456 789

## 📈 Change History

### Version 1.0.0 (Current - In Development)

- ✅ Initial module structure created
- ✅ 12 SQLAlchemy models implemented
- ✅ 11 Pydantic schemas defined
- ✅ Basic service layer structure
- ✅ Route organization completed
- ✅ Basic test coverage implemented
- ✅ Health check endpoint active
- 🚧 Core business logic implementation
- 🚧 License processing workflow
- 🚧 Regulatory integration
- 🚧 Document management system

### Version 1.1.0 (Planned)

- 📋 Complete license application workflow
- 📋 Business registration system
- 📋 License renewal automation
- 📋 Regulatory API integration
- 📋 Document upload and validation
- 📋 Payment processing integration
- 📋 Notification system
- 📋 Analytics dashboard
- 📋 Advanced security features
- 📋 Performance optimization

### Version 1.2.0 (Future)

- 📋 Advanced business intelligence
- 📋 Mobile API optimization
- 📋 Multi-language support
- 📋 Advanced reporting system
- 📋 Integration with national systems
- 📋 AI-powered compliance checking
- 📋 Blockchain license verification
- 📋 Advanced analytics
- 📋 Predictive maintenance
- 📋 Enhanced user experience

## 🎯 Future Roadmap

### Short Term (Next 3 Months)

- [ ] Implement core license application endpoints
- [ ] Develop business registration system
- [ ] Create license renewal workflow
- [ ] Integrate with regulatory APIs
- [ ] Implement document management
- [ ] Add payment processing
- [ ] Create notification system
- [ ] Develop admin dashboard

### Medium Term (3-6 Months)

- [ ] Advanced business analytics
- [ ] Mobile API optimization
- [ ] Multi-language support
- [ ] Enhanced security features
- [ ] Performance optimization
- [ ] Integration with tax systems
- [ ] Advanced reporting
- [ ] User experience improvements

### Long Term (6-12 Months)

- [ ] AI-powered compliance checking
- [ ] Blockchain license verification
- [ ] Predictive analytics
- [ ] Advanced business intelligence
- [ ] National system integration
- [ ] International compliance
- [ ] Advanced mobile features
- [ ] Real-time monitoring dashboard

---

_Technical documentation - SILA Commercial Module_ _Last updated: 2025-01-17 - SILA
Documentation Team_ _Status: Active Development - Core Implementation Phase_ _Next
review: 2025-02-17_
