export interface User {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  permissions?: string[];
  roles?: string[];
}
