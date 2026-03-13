import { citizenHttp } from '../api/citizenHttp';

interface CitizenProfile {
  id: string;
  full_name: string;
  birth_date?: string | null;
  gender?: string | null;
  vital_status?: string | null;
  id_number?: string | null;
  nif?: string | null;
  email?: string | null;
  phone?: string | null;
}

interface CitizenEvent {
  id: string;
  event_type: string;
  payload: any;
  created_at: string;
}

export const citizenAuthService = {
  async login(email: string, password: string) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await citizenHttp.post<{ access_token: string }>(
      'auth/login',
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    
    localStorage.setItem('citizen_token', response.data.access_token);
    return response.data.access_token;
  },

  async getProfile(): Promise<CitizenProfile> {
    const response = await citizenHttp.get<CitizenProfile>('citizen/profile');
    return response.data;
  },

  async getEvents(): Promise<CitizenEvent[]> {
    const response = await citizenHttp.get<CitizenEvent[]>('citizen/events');
    return response.data;
  },

  async logout() {
    localStorage.removeItem('citizen_token');
    return await citizenHttp.post('auth/logout');
  }
};
