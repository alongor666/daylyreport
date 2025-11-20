export type MetricKey = 'premium' | 'policy_count' | 'commission';
export type ComparisonMetric = 'premium' | 'count';

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface KpiWindowValue {
  day: number;
  last7d: number;
  last30d: number;
}

export interface KpiWindowsPayload {
  anchor_date: string;
  premium: KpiWindowValue;
  policy_count: KpiWindowValue;
  commission: KpiWindowValue;
  target_gap_day?: number;
}

export interface KpiWindowsParams {
  date?: string;
}

export interface WeekComparisonSeries {
  name: string;
  data: number[];
  dates: string[];
}

export interface WeekComparisonPayload {
  x_axis: string[];
  series: WeekComparisonSeries[];
  latest_date: string;
}

export interface WeekComparisonRequest {
  metric: ComparisonMetric;
  filters: Record<string, string>;
  date?: string;
}

export interface FilterOptionsPayload {
  [dimension: string]: string[] | Record<string, string[]>;
}

export interface StructuredFilterOptions {
  options: Record<string, string[]>;
  teamMapping: Record<string, string[]>;
}

export interface RefreshResponse {
  message: string;
  latest_date?: string;
}
