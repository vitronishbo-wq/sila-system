const FIXED_HOLIDAYS = [
  { month: 1, day: 1, name: 'Ano Novo' },
  { month: 2, day: 4, name: 'Dia do Inicio da Luta Armada' },
  { month: 3, day: 8, name: 'Dia Internacional da Mulher' },
  { month: 4, day: 4, name: 'Dia da Paz e Reconciliacao' },
  { month: 5, day: 1, name: 'Dia do Trabalhador' },
  { month: 9, day: 17, name: 'Dia do Heroi Nacional' },
  { month: 11, day: 2, name: 'Dia de Finados' },
  { month: 11, day: 11, name: 'Dia da Independencia' },
  { month: 12, day: 25, name: 'Natal' }
];

const pad = (value: number) => String(value).padStart(2, '0');

const formatDateKey = (date: Date) => {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
};

const addDays = (date: Date, days: number) => {
  const next = new Date(date);
  next.setDate(next.getDate() + days);
  return next;
};

const easterSunday = (year: number) => {
  const a = year % 19;
  const b = Math.floor(year / 100);
  const c = year % 100;
  const d = Math.floor(b / 4);
  const e = b % 4;
  const f = Math.floor((b + 8) / 25);
  const g = Math.floor((b - f + 1) / 3);
  const h = (19 * a + b - d - g + 15) % 30;
  const i = Math.floor(c / 4);
  const k = c % 4;
  const l = (32 + 2 * e + 2 * i - h - k) % 7;
  const m = Math.floor((a + 11 * h + 22 * l) / 451);
  const month = Math.floor((h + l - 7 * m + 114) / 31);
  const day = ((h + l - 7 * m + 114) % 31) + 1;
  return new Date(year, month - 1, day);
};

const getAngolaHolidays = (year: number) => {
  const holidays = FIXED_HOLIDAYS.map(({ month, day }) =>
    `${year}-${pad(month)}-${pad(day)}`
  );

  const easter = easterSunday(year);
  const goodFriday = addDays(easter, -2);
  const carnivalTuesday = addDays(easter, -47);
  holidays.push(formatDateKey(goodFriday));
  holidays.push(formatDateKey(carnivalTuesday));

  return Array.from(new Set(holidays));
};

const isBusinessDay = (date: Date, holidays: Set<string>) => {
  const weekday = date.getDay();
  if (weekday === 0 || weekday === 6) return false;
  return !holidays.has(formatDateKey(date));
};

export const estimateBusinessDays = (totalDays: number, startDate = new Date()) => {
  if (!totalDays || totalDays <= 0) return 0;

  const fullDays = Math.floor(totalDays);
  const remainder = totalDays - fullDays;
  const endDate = addDays(startDate, fullDays + (remainder > 0 ? 1 : 0));
  const years = new Set<number>([startDate.getFullYear(), endDate.getFullYear()]);
  const holidays = new Set<string>();
  years.forEach((year) => {
    getAngolaHolidays(year).forEach((day) => holidays.add(day));
  });

  let businessDays = 0;
  for (let i = 0; i < fullDays; i += 1) {
    const current = addDays(startDate, i);
    if (isBusinessDay(current, holidays)) {
      businessDays += 1;
    }
  }

  if (remainder > 0) {
    const current = addDays(startDate, fullDays);
    if (isBusinessDay(current, holidays)) {
      businessDays += remainder;
    }
  }

  return Math.max(1, Math.round(businessDays * 10) / 10);
};

