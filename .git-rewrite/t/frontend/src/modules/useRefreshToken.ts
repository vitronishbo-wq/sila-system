import { useEffect } from "react";

export function useRefreshToken(refresh: () => Promise<void>, tokenExp?: number) {
  useEffect(() => {
    if (!tokenExp) return;
    // Refresh 1 minute before expiration
    const now = Date.now() / 1000;
    const timeout = (tokenExp - now - 60) * 1000;
    if (timeout > 0) {
      const timer = setTimeout(() => {
        refresh();
      }, timeout);
      return () => clearTimeout(timer);
    }
  }, [tokenExp, refresh]);
}
