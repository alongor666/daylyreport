import axios from 'axios';

export const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000
});

export async function healthCheck() {
  const { data } = await apiClient.get('/health');
  return data;
}
