import http from '../api/http';

export interface DashboardMetrics {
    total_citizens: string;
    total_documents: string;
    pending_requests: string;
    avg_response_time: string;
    trends: {
        citizens: string;
        documents: string;
        requests: string;
        response_time: string;
    };
}

export interface NotificationItem {
    id: string;
    title: string;
    message: string;
    type: 'info' | 'warning' | 'success' | 'error' | 'document_update' | 'system';
    is_read: boolean;
    created_at: string;
    document_id?: string;
}

export interface RecentRequest {
    id: string;
    request_number?: string;
    citizen_name?: string;
    service_type: string;
    status: string;
    created_at: string;
    assigned_to?: string;
    priority?: string;
}

export interface DashboardData {
    metrics: DashboardMetrics;
    recent_events: any[];
    period: { start: string; end: string };
}

const dashboardService = {
    async getDashboard(): Promise<DashboardData> {
        try {
            const response = await http.get('/admin/dashboard/');
            return response.data;
        } catch {
            // Fallback: return structured mock when API unavailable
            return {
                metrics: {
                    total_citizens: '—',
                    total_documents: '—',
                    pending_requests: '—',
                    avg_response_time: '—',
                    trends: { citizens: '+0%', documents: '+0%', requests: '+0%', response_time: '+0%' }
                },
                recent_events: [],
                period: { start: new Date().toISOString(), end: new Date().toISOString() }
            };
        }
    },

    async getNotifications(): Promise<NotificationItem[]> {
        try {
            const response = await http.get('/citizen/notifications/');
            return response.data;
        } catch {
            return [];
        }
    },

    async getUnreadCount(): Promise<number> {
        try {
            const response = await http.get('/citizen/notifications/unread-count');
            return response.data.unread_count || 0;
        } catch {
            return 0;
        }
    },

    async markAsRead(notificationId: string): Promise<void> {
        await http.post(`/citizen/notifications/${notificationId}/read`);
    },

    async markAllAsRead(): Promise<void> {
        await http.post('/citizen/notifications/read-all');
    },

    async getRecentRequests(): Promise<RecentRequest[]> {
        try {
            const response = await http.get('/admin/requests/', { params: { limit: 10 } });
            return response.data;
        } catch {
            return [];
        }
    },

    async getRequestStats(): Promise<Record<string, number>> {
        try {
            const response = await http.get('/service-requests/statistics');
            return response.data?.by_status || {};
        } catch {
            return {};
        }
    }
};

export default dashboardService;
