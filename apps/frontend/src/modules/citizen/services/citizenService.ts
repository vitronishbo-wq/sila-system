import { citizenHttp } from "../../../api/citizenHttp";

export const citizenService = {
  getNotifications: () => citizenHttp.get("/citizen/notifications"),
  getUnreadCount: () => citizenHttp.get("/citizen/notifications/unread-count"),
};
