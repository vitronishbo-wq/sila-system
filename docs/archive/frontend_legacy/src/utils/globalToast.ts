type ToastData = {
  message: string;
  type?: 'success' | 'error' | 'info' | 'warning';
  link?: string;
};

type ToastFn = (data: ToastData) => void;

let globalToast: ToastFn | null = null;

export const setGlobalToast = (fn: ToastFn | null) => {
  globalToast = fn;
};

export const showGlobalToast = (data: ToastData) => {
  globalToast?.(data);
};
