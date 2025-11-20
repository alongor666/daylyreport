import axios from 'axios';
import type {
  ApiResponse,
  FilterOptionsPayload,
  KpiWindowsParams,
  KpiWindowsPayload,
  RefreshResponse,
  WeekComparisonPayload,
  WeekComparisonRequest
} from '@/types/api';

export const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000
});

export async function fetchKpiWindows(params?: KpiWindowsParams): Promise<ApiResponse<KpiWindowsPayload>> {
  const { data } = await apiClient.get<ApiResponse<KpiWindowsPayload>>('/kpi-windows', {
    params
  });
  return data;
}

export async function fetchWeekComparison(
  payload: WeekComparisonRequest
): Promise<ApiResponse<WeekComparisonPayload>> {
  const { data } = await apiClient.post<ApiResponse<WeekComparisonPayload>>('/week-comparison', payload);
  return data;
}

export async function fetchFilterOptions(): Promise<ApiResponse<FilterOptionsPayload>> {
  const { data } = await apiClient.get<ApiResponse<FilterOptionsPayload>>('/filter-options');
  return data;
}

export async function triggerRefresh(): Promise<ApiResponse<RefreshResponse>> {
  const { data } = await apiClient.post<ApiResponse<RefreshResponse>>('/refresh');
  return data;
}

export async function healthCheck() {
  const { data } = await apiClient.get('/health');
  return data;
}
