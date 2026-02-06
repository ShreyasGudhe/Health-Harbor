/**
 * VitalPlunder - API Service
 * 
 * Centralized API calls to the Flask backend.
 * Each module has its own set of API functions.
 * 
 * @author VitalPlunder Team
 */

import axios from 'axios';

// Base API URL - uses proxy in development
const API_BASE = '/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data?.error || 'Server error');
    } else if (error.request) {
      // Request made but no response
      throw new Error('Unable to reach server. Please check if backend is running.');
    } else {
      throw new Error('Request failed');
    }
  }
);

// =====================================================
// Storm Watch (Health Risk) API
// =====================================================
export const stormWatchAPI = {
  // Predict health risk
  predict: (healthData) => api.post('/storm-watch/predict', healthData),
  
  // Analyze risk factors
  analyze: (healthData) => api.post('/storm-watch/analyze', healthData),
  
  // Get risk level info
  getInfo: () => api.get('/storm-watch/info'),
};

// =====================================================
// Mind Compass (Mental Health) API
// =====================================================
export const mindCompassAPI = {
  // Analyze text for stress
  analyzeText: (text) => api.post('/mind-compass/analyze-text', { text }),
  
  // Analyze questionnaire
  analyzeQuestionnaire: (responses) => api.post('/mind-compass/analyze-questionnaire', responses),
  
  // Get coping techniques
  getCopingTechniques: () => api.get('/mind-compass/coping-techniques'),
  
  // Get check-in template
  getCheckInTemplate: () => api.get('/mind-compass/check-in-template'),
};

// =====================================================
// Captain's Orders (Lifestyle) API
// =====================================================
export const captainsOrdersAPI = {
  // Analyze habits
  analyze: (habits) => api.post('/captains-orders/analyze', habits),
  
  // Get recommendations
  getRecommendations: (habits) => api.post('/captains-orders/recommendations', habits),
  
  // Get daily orders
  getDailyOrders: (timeOfDay = 'morning') => 
    api.get(`/captains-orders/daily-orders?time=${timeOfDay}`),
  
  // Get habits template
  getHabitsTemplate: () => api.get('/captains-orders/habits-template'),
};

// =====================================================
// Supply Check (Medication) API
// =====================================================
export const supplyCheckAPI = {
  // Predict adherence
  predict: (medicationData) => api.post('/supply-check/predict', medicationData),
  
  // Analyze schedule
  analyzeSchedule: (medications) => 
    api.post('/supply-check/analyze-schedule', { medications }),
  
  // Get upcoming doses
  getUpcoming: (medications, hoursAhead = 24) => 
    api.post('/supply-check/upcoming', { medications, hours_ahead: hoursAhead }),
  
  // Calculate adherence score
  calculateScore: (history) => 
    api.post('/supply-check/adherence-score', { history }),
  
  // Get medication template
  getTemplate: () => api.get('/supply-check/medication-template'),
};

// =====================================================
// Night Watch (Sleep) API
// =====================================================
export const nightWatchAPI = {
  // Comprehensive analysis
  analyze: (sleepData) => api.post('/night-watch/analyze', sleepData),
  
  // Quick prediction
  predict: (sleepData) => api.post('/night-watch/predict', sleepData),
  
  // Calculate ideal bedtime
  getIdealBedtime: (wakeTime, targetHours = 8) => 
    api.get(`/night-watch/ideal-bedtime?wake_time=${wakeTime}&target_hours=${targetHours}`),
  
  // Get sleep cycles
  getSleepCycles: (bedtime, cycles = 6) => 
    api.get(`/night-watch/sleep-cycles?bedtime=${bedtime}&cycles=${cycles}`),
  
  // Get sleep template
  getTemplate: () => api.get('/night-watch/sleep-template'),
};

// =====================================================
// Galley Log (Nutrition) API
// =====================================================
export const galleyLogAPI = {
  // Classify food by name
  classifyFood: (foodName) => api.post('/galley-log/classify', { food_name: foodName }),
  
  // Classify food from image
  classifyImage: (formData) => 
    axios.post(`${API_BASE}/galley-log/classify-image`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(res => res.data),
  
  // Get nutrition info
  getNutrition: (category, portion = 1.0, name = null) => 
    api.post('/galley-log/nutrition', { 
      food_category: category, 
      portion_multiplier: portion,
      name 
    }),
  
  // Log a meal
  logMeal: (items, mealType = 'meal') => 
    api.post('/galley-log/log-meal', { items, meal_type: mealType }),
  
  // Get daily summary
  getDailySummary: (meals) => api.post('/galley-log/daily-summary', { meals }),
  
  // Get food categories
  getCategories: () => api.get('/galley-log/food-categories'),
  
  // Get daily goals
  getDailyGoals: () => api.get('/galley-log/daily-goals'),
};

// =====================================================
// Ship Doctor (Medical Docs) API
// =====================================================
export const shipDoctorAPI = {
  // Analyze image document
  analyzeImage: (formData) => 
    axios.post(`${API_BASE}/ship-doctor/analyze-image`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(res => res.data),
  
  // Analyze PDF document
  analyzePDF: (formData) => 
    axios.post(`${API_BASE}/ship-doctor/analyze-pdf`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(res => res.data),
  
  // Analyze text directly
  analyzeText: (text) => api.post('/ship-doctor/analyze-text', { text }),
  
  // Get disclaimer
  getDisclaimer: () => api.get('/ship-doctor/disclaimer'),
  
  // Get supported formats
  getSupportedFormats: () => api.get('/ship-doctor/supported-formats'),
};

// =====================================================
// General API
// =====================================================
export const generalAPI = {
  // Health check
  healthCheck: () => api.get('/health'),
  
  // Get API info
  getInfo: () => axios.get('/').then(res => res.data),
};

export default api;
