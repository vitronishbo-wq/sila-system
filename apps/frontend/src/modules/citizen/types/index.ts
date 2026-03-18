export interface Notification {
  id: string;
  title: string;
  message: string;
  read: boolean;
  created_at: string;
  type: 'INFO' | 'SUCCESS' | 'WARNING' | 'ERROR';
}
