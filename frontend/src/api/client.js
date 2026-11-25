const defaultBaseUrl = '/api';

export const apiConfig = {
  baseUrl: import.meta.env.VITE_API_BASE_URL || defaultBaseUrl
};

export async function apiRequest(path, options = {}) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  const response = await fetch(`${apiConfig.baseUrl}${normalizedPath}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  });

  if (!response.ok) {
    throw new Error(`API request failed with ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
