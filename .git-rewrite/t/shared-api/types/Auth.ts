export interface LoginRequest {
  email: string;
  password: string;
}

export interface Tokens {
  access_token: string;
  refresh_token?: string;
  expires_in?: number;
}
