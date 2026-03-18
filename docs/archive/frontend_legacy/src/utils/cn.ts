import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Utility to merge tailwind classes with support for conditional classes.
 * Leverages clsx for logic and tailwind-merge to prevent class conflicts.
 */
export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}
