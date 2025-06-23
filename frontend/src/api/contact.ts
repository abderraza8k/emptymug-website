import axios from 'axios';
import { ContactFormData, ApiResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const contactService = {
  async submitContact(data: ContactFormData): Promise<ApiResponse> {
    try {
      const response = await api.post('/api/contact', data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        return {
          success: false,
          message: error.response.data.message || 'Failed to send message',
        };
      }
      return {
        success: false,
        message: 'Network error. Please try again.',
      };
    }
  },
};
