export type AdminLevel = 'CENTRAL' | 'PROVINCIAL' | 'LOCAL';

export interface User {
    id: number;
    uuid?: string;
    email: string;
    full_name?: string;
    phone_number?: string;
    bi_number?: string;
    address?: string;
    birth_date?: string;
    gender?: string;
    is_active: boolean;
    is_verified: boolean;
    status?: string;
    administrative_level: AdminLevel;
    region_id?: number;
    roles: string[];
    created_at?: string;
    updated_at?: string;
    last_login?: string;
}
