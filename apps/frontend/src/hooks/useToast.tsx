import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import Toast from '../components/Toast';
import type { ToastData } from '../components/Toast';
import { setGlobalToast } from '../utils/globalToast';

interface ToastContextValue {
  toast: ToastData | null;
  stack: ToastData[];
  showToast: (data: ToastData) => void;
  hideToast: () => void;
  isClosing: boolean;
  progress: number;
  promoteToast: (index: number) => void;
  dismissToast: (index: number) => void;
  stackPulseAt: number | null;
  stackReorderAt: number | null;
}

const ToastContext = createContext<ToastContextValue | null>(null);

interface ToastProviderProps {
  children: React.ReactNode;
  durationMs?: number;
  maxStack?: number;
}

export const ToastProvider: React.FC<ToastProviderProps> = ({ children, durationMs = 4000, maxStack = 2 }) => {
  const [toast, setToast] = useState<ToastData | null>(null);
  const [queue, setQueue] = useState<ToastData[]>([]);
  const [isClosing, setIsClosing] = useState(false);
  const [progress, setProgress] = useState(100);
  const [stackPulseAt, setStackPulseAt] = useState<number | null>(null);
  const [stackReorderAt, setStackReorderAt] = useState<number | null>(null);
  const timerRef = useRef<number | null>(null);
  const rafRef = useRef<number | null>(null);
  const startRef = useRef<number | null>(null);
  const idRef = useRef(0);

  const clearTimer = () => {
    if (timerRef.current !== null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    if (rafRef.current !== null) {
      window.cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }
  };

  const hideToast = useCallback(() => {
    if (!toast) return;
    clearTimer();
    setIsClosing(true);
    window.setTimeout(() => {
      setToast(null);
      setIsClosing(false);
    }, 200);
  }, [toast]);

  const ensureId = (data: ToastData) => (
    data.id ? data : { ...data, id: `toast_${Date.now()}_${idRef.current++}` }
  );

  const showToast = useCallback((data: ToastData) => {
    const payload = ensureId(data);
    const effectiveMax = data.maxStack ?? maxStack;
    setQueue((prev) => {
      if (!toast) {
        setToast(payload);
        setIsClosing(false);
        return prev;
      }
      const nextQueue = [...prev, payload];
      return nextQueue.slice(0, Math.max(1, effectiveMax));
    });
  }, [toast, maxStack]);

  useEffect(() => {
    // Make toast available outside React (e.g. HTTP interceptors)
    setGlobalToast(showToast);
    return () => setGlobalToast(null);
  }, [showToast]);

  useEffect(() => {
    clearTimer();
    if (!toast) {
      if (queue.length > 0) {
        const [next, ...rest] = queue;
        setQueue(rest);
        setToast(next);
        setIsClosing(false);
        setProgress(100);
      }
      return;
    }
    const effectiveDuration = toast.durationMs ?? durationMs;
    startRef.current = performance.now();
    const tick = (now: number) => {
      if (!startRef.current) return;
      const elapsed = now - startRef.current;
      const remaining = Math.max(0, effectiveDuration - elapsed);
      setProgress((remaining / effectiveDuration) * 100);
      if (remaining > 0) {
        rafRef.current = window.requestAnimationFrame(tick);
      }
    };
    rafRef.current = window.requestAnimationFrame(tick);
    timerRef.current = window.setTimeout(() => {
      hideToast();
      timerRef.current = null;
    }, effectiveDuration);
  }, [toast, queue, durationMs, hideToast]);

  useEffect(() => () => clearTimer(), []);

  const promoteToast = useCallback((index: number) => {
    setQueue((prev) => {
      if (index < 0 || index >= prev.length) return prev;
      const selected = ensureId(prev[index]);
      const remaining = prev.filter((_, i) => i !== index);
      if (toast) {
        remaining.push(ensureId(toast));
      }
      setToast(selected);
      setIsClosing(false);
      setProgress(100);
      setStackPulseAt(Date.now());
      setStackReorderAt(Date.now());
      const effectiveMax = selected.maxStack ?? maxStack;
      return remaining.slice(0, Math.max(1, effectiveMax));
    });
  }, [toast, maxStack]);

  const dismissToast = useCallback((index: number) => {
    setQueue((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const value = useMemo(() => ({
    toast,
    stack: queue.slice(0, Math.max(1, maxStack)),
    showToast,
    hideToast,
    isClosing,
    progress,
    promoteToast,
    dismissToast,
    stackPulseAt,
    stackReorderAt,
  }), [toast, queue, showToast, hideToast, isClosing, progress, promoteToast, dismissToast, maxStack, stackPulseAt, stackReorderAt]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <Toast
        toast={toast}
        onClose={hideToast}
        isClosing={isClosing}
        progress={progress}
        stack={value.stack}
        onPromote={promoteToast}
        onDismiss={dismissToast}
        stackPulseAt={stackPulseAt}
        stackReorderAt={stackReorderAt}
      />
    </ToastContext.Provider>
  );
};

export const useToast = (options?: { durationMs?: number; maxStack?: number }) => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  const showToast = useCallback((data: ToastData) => {
    const durationMs = data.durationMs ?? options?.durationMs;
    const maxStack = data.maxStack ?? options?.maxStack;
    context.showToast({ ...data, durationMs, maxStack });
  }, [context, options?.durationMs, options?.maxStack]);
  return {
    toast: context.toast,
    stack: context.stack,
    showToast,
    hideToast: context.hideToast,
    isClosing: context.isClosing,
    progress: context.progress,
    promoteToast: context.promoteToast,
    dismissToast: context.dismissToast,
    stackPulseAt: context.stackPulseAt,
    stackReorderAt: context.stackReorderAt,
  };
};
