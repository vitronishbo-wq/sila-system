export interface AccessToken {
  access_token: string;
  expires_in?: number;
}

export interface RefreshToken {
  refresh_token: string;
}
