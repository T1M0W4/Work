import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
// Импортируйте другие редьюсеры

export default configureStore({
  reducer: {
    auth: authReducer,
    // Добавьте другие редьюсеры
  },
});