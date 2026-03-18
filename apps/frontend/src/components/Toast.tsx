import React from 'react';

export type ToastType = 'success' | 'error' | 'info';

export interface ToastData {
  id?: string;
  type?: ToastType;
  message: string;
  link?: string;
  durationMs?: number;
  maxStack?: number;
}

interface ToastProps {
  toast: ToastData | null;
  onClose?: () => void;
  isClosing?: boolean;
  progress?: number;
  stack?: ToastData[];
  onPromote?: (index: number) => void;
  onDismiss?: (index: number) => void;
  stackPulseAt?: number | null;
  stackReorderAt?: number | null;
}

const Toast: React.FC<ToastProps> = ({
  toast,
  onClose,
  isClosing = false,
  progress = 100,
  stack = [],
  onPromote,
  onDismiss,
  stackPulseAt = null,
  stackReorderAt = null,
}) => {
  if (!toast) return null;
  const type = toast.type || 'success';
  const styles = {
    success: 'bg-emerald-600 text-white',
    error: 'bg-red-600 text-white',
    info: 'bg-blue-600 text-white',
  };
  const [visible, setVisible] = React.useState(false);

  React.useEffect(() => {
    if (!toast) return;
    const id = window.requestAnimationFrame(() => setVisible(true));
    return () => window.cancelAnimationFrame(id);
  }, [toast]);

  React.useEffect(() => {
    if (isClosing) {
      setVisible(false);
    }
  }, [isClosing]);

  const stackPulseActive = stackPulseAt ? (Date.now() - stackPulseAt < 800) : false;
  const [stackReorderActive, setStackReorderActive] = React.useState(false);

  React.useEffect(() => {
    if (!stackReorderAt) return;
    setStackReorderActive(true);
    const timer = window.setTimeout(() => setStackReorderActive(false), 260);
    return () => window.clearTimeout(timer);
  }, [stackReorderAt]);

  const stackRefs = React.useRef(new Map<string, HTMLDivElement>());
  const stackPositions = React.useRef(new Map<string, DOMRect>());
  const mainRef = React.useRef<HTMLDivElement>(null);
  const mainPositions = React.useRef<DOMRect | null>(null);
  const mainFlipActive = React.useRef(false);

  React.useLayoutEffect(() => {
    if (!stack.length) return;
    const nextPositions = new Map<string, DOMRect>();
    stack.forEach((item) => {
      const el = item.id ? stackRefs.current.get(item.id) : null;
      if (!el) return;
      nextPositions.set(item.id!, el.getBoundingClientRect());
    });
    nextPositions.forEach((rect, id) => {
      const prev = stackPositions.current.get(id);
      if (!prev) return;
      const deltaY = prev.top - rect.top;
      const deltaX = prev.left - rect.left;
      if (Math.abs(deltaX) < 1 && Math.abs(deltaY) < 1) return;
      const el = stackRefs.current.get(id);
      if (!el) return;
      el.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
      el.style.transition = 'transform 0s';
      window.requestAnimationFrame(() => {
        el.style.transition = 'transform 220ms cubic-bezier(0.22, 1, 0.36, 1)';
        el.style.transform = 'translate(0px, 0px)';
      });
    });
    stackPositions.current = nextPositions;
  }, [stack]);

  React.useLayoutEffect(() => {
    if (!toast) {
      mainPositions.current = null;
      return;
    }
    const el = mainRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const prev = mainPositions.current;
    if (prev) {
      const deltaX = prev.left - rect.left;
      const deltaY = prev.top - rect.top;
      if (Math.abs(deltaX) > 1 || Math.abs(deltaY) > 1) {
        mainFlipActive.current = true;
        el.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        el.style.transition = 'transform 0s';
        window.requestAnimationFrame(() => {
          el.style.transition = 'transform 220ms cubic-bezier(0.22, 1, 0.36, 1)';
          el.style.transform = 'translate(0px, 0px)';
          window.setTimeout(() => {
            mainFlipActive.current = false;
          }, 240);
        });
      }
    }
    mainPositions.current = rect;
  }, [toast?.id, stack.length]);

  React.useEffect(() => {
    const el = mainRef.current;
    if (!el) return;
    if (mainFlipActive.current) return;
    if (visible && !isClosing) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(8px)';
      el.style.transition = 'opacity 140ms ease, transform 200ms cubic-bezier(0.22, 1, 0.36, 1)';
      window.requestAnimationFrame(() => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0px)';
      });
      return;
    }
    if (isClosing) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(8px)';
      el.style.transition = 'opacity 120ms ease, transform 180ms ease';
    }
  }, [visible, isClosing, toast?.id]);

  return (
    <div className="fixed bottom-6 right-6 flex flex-col items-end gap-2">
      {stack.map((item, index) => (
        <div
          key={item.id || `${item.message}-${index}`}
          ref={(el) => {
            if (item.id) {
              if (el) stackRefs.current.set(item.id, el);
              else stackRefs.current.delete(item.id);
            }
          }}
          className={`rounded-xl px-4 py-2 text-xs font-semibold shadow-lg bg-slate-700 text-white/90 flex items-center gap-2 transition-colors duration-200 transition-opacity ${
            stackPulseActive ? 'animate-pulse' : ''
          } ${stackReorderActive ? 'opacity-60' : 'opacity-80'}`}
          style={{ willChange: 'transform' }}
        >
          <button
            type="button"
            onClick={() => onPromote?.(index)}
            className="flex-1 text-left hover:text-white transition-colors"
            title="Abrir toast"
          >
            {item.message}
          </button>
          <button
            type="button"
            onClick={() => onDismiss?.(index)}
            className="text-white/70 hover:text-white transition-colors"
            aria-label="Fechar"
            title="Fechar toast"
          >
            <i className="fa-solid fa-xmark" />
          </button>
        </div>
      ))}
      <div
        ref={mainRef}
        className={`relative overflow-hidden rounded-xl px-4 py-3 text-sm font-semibold shadow-lg ${styles[type]}`}
        style={{ willChange: 'transform, opacity' }}
      >
        <div className="flex items-center gap-3">
          <span>{toast.message}</span>
          {toast.link && (
            <a
              href={toast.link}
              className="underline text-white"
              target="_blank"
              rel="noreferrer"
            >
              Download
            </a>
          )}
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="ml-2 text-white/80 hover:text-white transition-colors"
              aria-label="Fechar"
            >
              <i className="fa-solid fa-xmark" />
            </button>
          )}
        </div>
        <div className="absolute bottom-0 left-0 h-1 bg-white/70" style={{ width: `${Math.max(0, Math.min(100, progress))}%` }} />
      </div>
    </div>
  );
};

export default Toast;
