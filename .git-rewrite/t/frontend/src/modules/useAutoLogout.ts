import { useEffect } from "react";

export function useAutoLogout(onLogout: () => void, tokenExp?: number) {
  useEffect(() => {
    if (!tokenExp) return;
    const now = Date.now() / 1000;
    const timeout = (tokenExp - now) * 1000;
    if (timeout > 0) {
      const timer = setTimeout(onLogout, timeout);
      return () => clearTimeout(timer);
    } else {
      onLogout();
    }
  }, [tokenExp, onLogout]);
}
