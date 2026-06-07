import { useState, useEffect } from "react";
import { citizenService } from "@/modules/citizen/services";

export const useNotifications = () => {
  const [notifications, setNotifications] = useState([]);

  const fetch = async () => {
    try {
      const { data } = await citizenService.getNotifications();
      setNotifications(data);
    } catch (error) {
      console.error("Erro ao buscar notificações", error);
    }
  };

  useEffect(() => { fetch(); }, []);
  return { notifications, refetch: fetch };
};
