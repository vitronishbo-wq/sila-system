export const formatDate = (date: string | Date): string => {
  return new Date(date).toLocaleDateString("pt-AO", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
};

export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat("pt-AO", {
    style: "currency",
    currency: "AOA",
  }).format(value);
};

export const truncate = (text: string, length: number): string => {
  return text.length > length ? text.slice(0, length) + "..." : text;
};
