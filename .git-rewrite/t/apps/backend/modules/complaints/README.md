# Complaints Module

# SILA System - Backend

## 📋 Description

The Complaints module manages the complete lifecycle of citizen complaints and service
requests within the SILA system. It provides a comprehensive platform for submitting,
tracking, processing, and resolving complaints from citizens, ensuring transparency,
accountability, and efficient service delivery across municipal departments.

## 🚀 Core Functionalities

- 📝 **Complaint Submission** - Multi-channel complaint registration (web, mobile,
  in-person)
- 🔄 **Status Tracking** - Real-time complaint status updates and notifications
- 📊 **Case Management** - Comprehensive case assignment and workflow management
- 🏢 **Department Integration** - Seamless routing to relevant municipal departments
- 📈 **Analytics Dashboard** - Comprehensive reporting and insights
- 🔍 **Search & Filter** - Advanced search capabilities for complaints
- 📱 **Mobile Support** - Mobile-optimized interface for field agents
- 📋 **Escalation Management** - Automatic escalation based on priority and SLA

## 📡 Available Endpoints

| Method | Endpoint                    | Description                    | Authentication | Rate Limit | Status    |
| ------ | --------------------------- | ------------------------------ | -------------- | ---------- | --------- |
| `GET`  | `/complaints/ping`          | Module health check            | ❌ Public      | 1000/hour  | ✅ Active |
| `POST` | `/complaints`               | Submit new complaint           | ✅ Required    | 100/hour   | ✅ Active |
| `GET`  | `/complaints`               | List complaints (filtered)     | ✅ Required    | 500/hour   | ✅ Active |
| `GET`  | `/complaints/{id}`          | Get complaint details          | ✅ Required    | 500/hour   | ✅ Active |
| `PUT`  | `/complaints/{id}`          | Update complaint               | ✅ Required    | 100/hour   | ✅ Active |
| `POST` | `/complaints/{id}/assign`   | Assign complaint to department | ✅ Required    | 100/hour   | ✅ Active |
| `POST` | `/complaints/{id}/resolve`  | Mark complaint as resolved     | ✅ Required    | 50/hour    | ✅ Active |
| `GET`  | `/complaints/categories`    | List complaint categories      | ❌ Public      | 1000/hour  | ✅ Active |
| `GET`  | `/complaints/departments`   | List handling departments      | ❌ Public      | 1000/hour  | ✅ Active |
| `GET`  | `/complaints/status`        | List possible statuses         | ❌ Public      | 1000/hour  | ✅ Active |
| `POST` | `/complaints/{id}/comment`  | Add comment to complaint       | ✅ Required    | 200/hour   | ✅ Active |
| `GET`  | `/complaints/{id}/history`  | Get complaint history          | ✅ Required    | 500/hour   | ✅ Active |
| `POST` | `/complaints/{id}/escalate` | Escalate complaint             | ✅ Required    | 50/hour    | ✅ Active |

## 🔧 Configuration

### Technology Stack

- **Framework:** FastAPI with async support
- **Database:** PostgreSQL with optimized queries
- **Authentication:** JWT with role-based access
- **File Storage:** S3-compatible storage for attachments
- **Notifications:** Email, SMS, and push notifications
- **Search:** Full-text search capabilities
- **Analytics:** Real-time metrics and reporting

### Environment Variables

```bash
# Complaints Module Configuration
COMPLAINTS_DB_URL=postgresql://user:pass@localhost/sila_complaints
COMPLAINTS_JWT_SECRET_KEY=your-secret-key
COMPLAINTS_JWT_ALGORITHM=HS256
COMPLAINTS_ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage Configuration
COMPLAINTS_ATTACHMENTS_BUCKET=sila-complaints-attachments
COMPLAINTS_MAX_FILE_SIZE=10485760  # 10MB
COMPLAINTS_ALLOWED_EXTENSIONS=jpg,jpeg,png,pdf,doc,docx

# Notification Configuration
COMPLAINTS_SMTP_HOST=smtp.gov.ao
COMPLAINTS_SMTP_PORT=587
COMPLAINTS_SMS_PROVIDER=twilio
COMPLAINTS_PUSH_NOTIFICATIONS_ENABLED=true

# SLA Configuration
COMPLAINTS_DEFAULT_SLA_HOURS=72
COMPLAINTS_URGENT_SLA_HOURS=24
COMPLAINTS_ESCALATION_THRESHOLD_HOURS=48

# Search Configuration
COMPLAINTS_SEARCH_INDEX=complaints_index
COMPLAINTS_SEARCH_ENABLED=true
COMPLAINTS_MIN_SEARCH_LENGTH=3
```

## 🗂️ Module Structure

```
complaints/
├── __init__.py          # Module initialization (3075 lines)
├── endpoints.py         # API route definitions (1 endpoint)
├── models/              # SQLAlchemy models
│   ├── __init__.py
│   ├── complaint.py     # Main complaint model
│   ├── category.py      # Complaint category model
│   ├── department.py    # Department model
│   ├── status.py        # Status tracking model
│   ├── assignment.py    # Assignment tracking model
│   ├── comment.py       # Comment model
│   ├── attachment.py    # File attachment model
│   ├── escalation.py    # Escalation model
│   ├── notification.py  # Notification model
│   ├── audit.py         # Audit trail model
│   └── priority.py      # Priority level model
├── schemas/             # Pydantic schemas
│   ├── __init__.py
│   ├── complaint.py     # Complaint validation schemas
│   ├── category.py      # Category validation schemas
│   ├── department.py    # Department validation schemas
│   ├── status.py        # Status validation schemas
│   ├── assignment.py    # Assignment validation schemas
│   ├── comment.py       # Comment validation schemas
│   ├── attachment.py    # Attachment validation schemas
│   ├── escalation.py    # Escalation validation schemas
│   ├── notification.py  # Notification validation schemas
│   └── response.py      # Standard response schemas
├── services/            # Business logic
│   ├── __init__.py
│   ├── complaint_service.py  # Core complaint operations
│   ├── assignment_service.py # Assignment logic
│   ├── notification_service.py # Notification handling
│   ├── escalation_service.py # Escalation logic
│   ├── search_service.py     # Search functionality
│   └── analytics_service.py  # Analytics and reporting
├── routes/              # API routes
│   ├── __init__.py
│   ├── complaints.py    # Main complaint routes
│   ├── categories.py    # Category management routes
│   ├── departments.py   # Department routes
│   ├── assignments.py   # Assignment routes
│   ├── comments.py      # Comment routes
│   ├── attachments.py   # File attachment routes
│   ├── escalations.py   # Escalation routes
│   └── analytics.py     # Analytics routes
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── validators.py    # Custom validators
│   ├── helpers.py       # Helper functions
│   ├── notifications.py # Notification utilities
│   ├── file_handler.py  # File handling utilities
│   └── search.py        # Search utilities
├── exceptions/          # Custom exceptions
│   ├── __init__.py
│   ├── complaint.py     # Complaint-specific exceptions
│   ├── validation.py    # Validation exceptions
│   └── authorization.py # Authorization exceptions
├── tests/               # Test files
│   ├── __init__.py
│   ├── test_complaints.py # Complaint tests
│   ├── test_services.py # Service tests
│   ├── test_routes.py   # Route tests
│   └── fixtures.py      # Test fixtures
└── README.md            # This documentation
```

## 📚 Usage Examples

### FastAPI Integration Example

```python
from fastapi import FastAPI, Depends, HTTPException
from app.modules.complaints import router
from app.modules.complaints.schemas import ComplaintCreate, ComplaintResponse
from app.modules.complaints.services import ComplaintService
from app.core.auth import get_current_user

app = FastAPI(title="SILA Complaints API")
app.include_router(router, prefix="/complaints", tags=["complaints"])

@app.post("/complaints", response_model=ComplaintResponse)
async def create_complaint(
    complaint: ComplaintCreate,
    current_user = Depends(get_current_user)
):
    service = ComplaintService()
    try:
        new_complaint = await service.create_complaint(complaint, current_user.id)
        return new_complaint
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/complaints/{complaint_id}")
async def get_complaint(
    complaint_id: str,
    current_user = Depends(get_current_user)
):
    service = ComplaintService()
    complaint = await service.get_complaint_by_id(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint
```

### Complete HTTP Client Example

```bash
# Health check (public)
curl -X GET "http://localhost:8000/complaints/ping" \
  -H "Accept: application/json"

# Get authentication token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "citizen@example.com",
    "password": "secure_password"
  }'

# Submit new complaint (authenticated)
curl -X POST "http://localhost:8000/complaints" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Street Light Not Working",
    "description": "The street light at the corner of Rua Principal and Avenida Central has been not working for the past week. This creates a safety hazard for pedestrians at night.",
    "category_id": "street_lighting",
    "priority": "medium",
    "location": {
      "address": "Rua Principal, 123, Luanda",
      "latitude": -8.838333,
      "longitude": 13.234444
    },
    "contact_info": {
      "phone": "+244 923 456 789",
      "email": "citizen@example.com"
    }
  }'

# List complaints (authenticated)
curl -X GET "http://localhost:8000/complaints?status=pending&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Get specific complaint details (authenticated)
curl -X GET "http://localhost:8000/complaints/123" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Assign complaint to department (authenticated)
curl -X POST "http://localhost:8000/complaints/123/assign" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "department_id": "public_works",
    "assigned_to": "technician_id",
    "notes": "Assign to senior technician for urgent repair"
  }'

# Add comment to complaint (authenticated)
curl -X POST "http://localhost:8000/complaints/123/comment" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "Technician has been dispatched to investigate the issue.",
    "is_internal": false
  }'

# Resolve complaint (authenticated)
curl -X POST "http://localhost:8000/complaints/123/resolve" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resolution": "Street light has been repaired and is now functioning properly.",
    "resolution_code": "fixed"
  }'
```

### Frontend Integration Example

```typescript
// complaints-api.ts
import { apiClient } from '@/lib/api-client';

export interface Complaint {
  id: string;
  title: string;
  description: string;
  category: {
    id: string;
    name: string;
  };
  status: 'pending' | 'assigned' | 'in_progress' | 'resolved' | 'closed';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  location: {
    address: string;
    latitude?: number;
    longitude?: number;
  };
  created_at: string;
  updated_at: string;
  assigned_to?: {
    id: string;
    name: string;
    department: string;
  };
  comments: Array<{
    id: string;
    comment: string;
    created_at: string;
    author: string;
  }>;
}

export interface ComplaintCreate {
  title: string;
  description: string;
  category_id: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  location: {
    address: string;
    latitude?: number;
    longitude?: number;
  };
  contact_info: {
    phone: string;
    email: string;
  };
}

export const complaintsAPI = {
  // Submit new complaint
  async createComplaint(complaintData: ComplaintCreate): Promise<Complaint> {
    const response = await apiClient.post('/complaints', complaintData);
    return response.data;
  },

  // Get user's complaints
  async getUserComplaints(filters?: {
    status?: string;
    category?: string;
    limit?: number;
    offset?: number;
  }): Promise<{ complaints: Complaint[]; total: number }> {
    const response = await apiClient.get('/complaints', { params: filters });
    return response.data;
  },

  // Get specific complaint
  async getComplaint(complaintId: string): Promise<Complaint> {
    const response = await apiClient.get(`/complaints/${complaintId}`);
    return response.data;
  },

  // Add comment to complaint
  async addComment(complaintId: string, comment: string, isInternal = false): Promise<void> {
    await apiClient.post(`/complaints/${complaintId}/comment`, {
      comment,
      is_internal: isInternal
    });
  },

  // Get complaint categories
  async getCategories(): Promise<Array<{ id: string; name: string; description: string }>> {
    const response = await apiClient.get('/complaints/categories');
    return response.data;
  }
};

// React component example
import React, { useState, useEffect } from 'react';
import { complaintsAPI, Complaint } from '@/features/complaints/api';

export const ComplaintsList: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const loadComplaints = async () => {
      try {
        const { complaints: userComplaints } = await complaintsAPI.getUserComplaints(
          filter !== 'all' ? { status: filter } : undefined
        );
        setComplaints(userComplaints);
      } catch (error) {
        console.error('Error loading complaints:', error);
      } finally {
        setLoading(false);
      }
    };

    loadComplaints();
  }, [filter]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'yellow';
      case 'assigned': return 'blue';
      case 'in_progress': return 'orange';
      case 'resolved': return 'green';
      case 'closed': return 'gray';
      default: return 'gray';
    }
  };

  if (loading) return <div>Loading complaints...</div>;

  return (
    <div className="complaints-list">
      <h2>My Complaints</h2>
      <div className="filters">
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All Status</option>
          <option value="pending">Pending</option>
          <option value="assigned">Assigned</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
        </select>
      </div>
      <div className="complaints-grid">
        {complaints.map(complaint => (
          <div key={complaint.id} className="complaint-card">
            <h3>{complaint.title}</h3>
            <p>{complaint.description}</p>
            <div className="complaint-meta">
              <span className={`status ${complaint.status}`}>
                {complaint.status.replace('_', ' ')}
              </span>
              <span className="priority">{complaint.priority}</span>
              <span className="date">
                {new Date(complaint.created_at).toLocaleDateString()}
              </span>
            </div>
            <div className="complaint-location">
              📍 {complaint.location.address}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

## 🔗 Dependencies

### Internal Dependencies

- **FastAPI** - Web framework with async support
- **SQLAlchemy** - ORM for complaint models
- **Pydantic** - Data validation and serialization
- **Alembic** - Database migrations
- **Redis** - Caching and session management
- **Celery** - Background task processing
- **Boto3** - S3 integration for file attachments

### Module Dependencies

- `app.core.auth` - Authentication and authorization
- `app.db.session` - Database session management
- `app.models.base` - Base model classes
- `app.core.config` - Configuration management
- `app.core.security` - Security utilities
- `app.modules.notifications` - Notification system
- `app.modules.users` - User management
- `app.modules.departments` - Department management

### External Dependencies

- **SMTP Server** - Email notifications
- **SMS Gateway** - SMS notifications (Twilio)
- **Push Notification Service** - Mobile push notifications
- **S3 Storage** - File attachment storage
- **Elasticsearch** - Full-text search
- **PostgreSQL** - Primary database

## ⚠️ Important Observations

### Development Environment

- **Complex workflows** - Multi-step complaint processing
- **File handling** - Attachment upload and validation
- **Notification system** - Multi-channel notifications
- **Search functionality** - Advanced search capabilities
- **Role-based access** - Different permissions for different user types

### Production Environment

- **High availability** - Critical citizen service
- **Data privacy** - Sensitive citizen information
- **Performance optimization** - Fast response times required
- **Scalability** - Handle high volume of complaints
- **Monitoring** - Real-time system health monitoring
- **Backup strategy** - Regular data backups

### Security Considerations

- **Data protection** - Encrypt sensitive citizen data
- **Access control** - Role-based permissions
- **Audit logging** - Complete audit trail
- **File security** - Secure file upload and storage
- **Input validation** - Prevent injection attacks
- **Rate limiting** - Prevent abuse of the system

### Performance Considerations

- **Database optimization** - Efficient queries for large datasets
- **Caching strategy** - Cache frequently accessed data
- **Search optimization** - Fast search capabilities
- **File handling** - Efficient file upload/download
- **Notification queuing** - Async notification processing
- **Load balancing** - Distribute load across servers

## 🔒 Security Implementation

### Implemented Security Measures

- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Role-Based Access Control** - Different permissions for different roles
- ✅ **Input Validation** - Comprehensive data validation
- ✅ **SQL Injection Protection** - SQLAlchemy ORM protection
- ✅ **File Upload Security** - Secure file handling
- ✅ **Audit Logging** - Complete audit trail
- ✅ **Rate Limiting** - API endpoint protection
- ✅ **CORS Configuration** - Cross-origin security

### Security Recommendations

- 🔒 **Data Encryption** - Encrypt sensitive citizen data
- 🔒 **Enhanced Audit** - Detailed logging of all actions
- 🔒 **Security Headers** - Implement security HTTP headers
- 🔒 **Regular Security Audits** - Periodic security assessments
- 🔒 **Penetration Testing** - Regular security testing
- 🔒 **Security Training** - Team security awareness training

## 📊 Analytics and Monitoring

### Key Performance Indicators (KPIs)

- **Complaint Resolution Time** - Average time to resolve complaints
- **First Response Time** - Time to first response on new complaints
- **Customer Satisfaction** - Citizen satisfaction scores
- **Department Performance** - Performance by department
- **SLA Compliance** - Percentage of complaints resolved within SLA
- **System Uptime** - Overall system availability

### Monitoring Metrics

```python
# Complaints module metrics
COMPLAINTS_METRICS = {
    'complaints_received': Counter('complaints_received_total'),
    'complaints_resolved': Counter('complaints_resolved_total'),
    'resolution_time': Histogram('complaint_resolution_time_hours'),
    'first_response_time': Histogram('complaint_first_response_time_minutes'),
    'sla_compliance': Gauge('complaints_sla_compliance_percentage'),
    'customer_satisfaction': Gauge('complaints_customer_satisfaction_score'),
    'department_performance': Gauge('complaints_department_performance_score'),
    'api_requests': Counter('complaints_api_requests_total'),
    'api_response_time': Histogram('complaints_api_response_time_seconds')
}
```

### Health Checks

```python
@app.get("/complaints/health")
async def health_check():
    checks = {
        "database": await check_database_connection(),
        "redis": await check_redis_connection(),
        "storage": await check_storage_connection(),
        "notifications": await check_notification_services(),
        "search": await check_search_service()
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
# Complaints module alerts
alerts:
  - name: "High Resolution Time"
    condition: "complaint_resolution_time > 72h"
    severity: "warning"

  - name: "Low SLA Compliance"
    condition: "complaints_sla_compliance < 80%"
    severity: "critical"

  - name: "System Error Rate"
    condition: "complaints_api_error_rate > 5%"
    severity: "warning"

  - name: "Database Connection Issues"
    condition: "complaints_database_connection_failed"
    severity: "critical"

  - name: "Notification Service Down"
    condition: "complaints_notification_service_unavailable"
    severity: "warning"
```

## 🔄 Workflow Diagrams

### Complaint Processing Workflow

```mermaid
flowchart TD
    A[Citizen Submits Complaint] --> B[Validation & Screening]
    B --> C{Valid Complaint?}
    C -->|No| D[Reject with Reason]
    C -->|Yes| E[Assign Category & Priority]
    E --> F[Auto-Assign to Department]
    F --> G[Notify Assigned Department]
    G --> H[Department Acknowledges]
    H --> I[Investigation & Assessment]
    I --> J[Update Status & Comments]
    J --> K{Resolution Found?}
    K -->|No| L[Escalate if Needed]
    L --> M[Continue Investigation]
    M --> K
    K -->|Yes| N[Implement Solution]
    N --> O[Notify Citizen]
    O --> P[Citizen Confirms Resolution]
    P --> Q{Citizen Satisfied?}
    Q -->|No| R[Reopen Complaint]
    R --> I
    Q -->|Yes| S[Mark as Resolved]
    S --> T[Archive & Analytics]
```

### Escalation Workflow

```mermaid
flowchart TD
    A[Complaint Assigned] --> B[Monitor SLA]
    B --> C{SLA Breach Risk?}
    C -->|No| B
    C -->|Yes| D[Check Escalation Rules]
    D --> E{Auto-Escalate?}
    E -->|No| F[Notify Supervisor]
    F --> G{Manual Escalation?}
    G -->|No| H[Continue Monitoring]
    H --> B
    G -->|Yes| I[Escalate to Higher Level]
    E -->|Yes| I
    I --> J[Assign to Senior Staff]
    J --> K[Update Priority]
    K --> L[Notify All Stakeholders]
    L --> M[Continue with Higher Authority]
```

## 👥 Responsibilities

### Development Team

- **Module Owner:** SILA Complaints Team
- **Lead Developer:** Complaints Module Lead
- **Backend Developers:** 3 developers
- **Frontend Developers:** 2 developers
- **QA Engineer:** 2 testers
- **DevOps Engineer:** Infrastructure support
- **Product Manager:** Complaints Product Owner

### Contact Information

- **Email:** dev@sila.gov.ao
- **Slack:** #sila-backend-complaints
- **Jira:** SILA-COMPLAINTS
- **Documentation:** https://docs.sila.gov.ao/complaints

### Support Hours

- **Development Support:** Monday - Friday, 9:00 - 18:00 (UTC+1)
- **Production Support:** 24/7 on-call rotation
- **Emergency Contact:** +244 923 456 789

## 📈 Change History

### Version 1.0.0 (Current)

- ✅ Initial module structure created
- ✅ Basic complaint CRUD operations
- ✅ Department assignment system
- ✅ Status tracking functionality
- ✅ Comment system implemented
- ✅ File attachment support
- ✅ Basic notification system
- ✅ Search functionality
- ✅ Analytics dashboard
- ✅ Mobile API endpoints

### Version 1.1.0 (Planned)

- 📋 Advanced workflow automation
- 📋 AI-powered categorization
- 📋 Enhanced analytics
- 📋 Multi-language support
- 📋 Advanced reporting
- 📋 Integration with external systems
- 📋 Enhanced mobile features
- 📋 Voice complaint submission
- 📋 Image recognition for issues
- 📋 Predictive analytics

### Version 1.2.0 (Future)

- 📋 Machine learning for prioritization
- 📋 Advanced citizen engagement
- 📋 Real-time collaboration
- 📋 Blockchain for transparency
- 📋 IoT integration
- 📋 Advanced security features
- 📋 Performance optimization
- 📋 International expansion
- 📋 API versioning
- 📋 Advanced monitoring

## 🎯 Future Roadmap

### Short Term (Next 3 Months)

- [ ] Implement advanced workflow automation
- [ ] Add AI-powered categorization
- [ ] Enhance analytics dashboard
- [ ] Implement multi-language support
- [ ] Add advanced reporting features
- [ ] Integrate with external municipal systems
- [ ] Enhance mobile application
- [ ] Add voice complaint submission

### Medium Term (3-6 Months)

- [ ] Implement image recognition for issues
- [ ] Add predictive analytics
- [ ] Develop machine learning prioritization
- [ ] Enhance citizen engagement features
- [ ] Implement real-time collaboration
- [ ] Add blockchain transparency features
- [ ] Integrate IoT sensors
- [ ] Optimize performance

### Long Term (6-12 Months)

- [ ] Advanced security features
- [ ] International expansion support
- [ ] API versioning implementation
- [ ] Advanced monitoring dashboard
- [ ] Automated testing improvements
- [ ] Documentation automation
- [ ] Performance optimization
- [ ] Scalability enhancements

---

_Technical documentation - SILA Complaints Module_ _Last updated: 2025-01-17 - SILA
Documentation Team_ _Status: Production Ready - Core Citizen Service_ _Next review:
2025-02-17_
