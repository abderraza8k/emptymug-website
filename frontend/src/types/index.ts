export interface ContactFormData {
  fullName: string;
  email: string;
  phoneNumber?: string;
  countryCode: string;
  message: string;
}

export interface Country {
  code: string;
  name: string;
  dialCode: string;
  flag: string;
}

export interface ApiResponse {
  success: boolean;
  message: string;
}
