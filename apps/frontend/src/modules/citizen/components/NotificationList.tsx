import React from 'react';
import { useNotifications } from '../hooks/useNotifications';
import { Notification } from '../types';

export const NotificationList: React.FC = () => {
  const { notifications, refetch } = useNotifications();

  return (
    <div className="space-y-4 p-4">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Minhas Notificações</h2>
        <button onClick={refetch} className="text-sm bg-blue-600 text-white px-3 py-1 rounded">Atualizar</button>
      </div>
      {notifications.length === 0 ? (
        <p className="text-gray-500 text-center">Nenhuma notificação encontrada.</p>
      ) : (
        notifications.map((n: Notification) => (
          <div key={n.id} className={`p-4 border-l-4 rounded shadow-sm ${n.read ? 'bg-gray-50 border-gray-300' : 'bg-white border-blue-600'}`}>
            <div className="flex justify-between">
              <span className="font-semibold text-lg">{n.title}</span>
              <span className="text-xs text-gray-400">{new Date(n.created_at).toLocaleDateString()}</span>
            </div>
            <p className="text-gray-600 mt-1">{n.message}</p>
          </div>
        ))
      )}
    </div>
  );
};
