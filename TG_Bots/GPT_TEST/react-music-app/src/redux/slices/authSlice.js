import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

export const login = createAsyncThunk('auth/login', async (credentials) => {
  const response = await axios.post('http://localhost:8000/api/users/token/', credentials);
  return response.data;
});

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    token: null,
    status: 'idle',
    error: null,
  },
  reducers: {
    logout(state) {
      state.token = null;
    },
  },
  extraReducers: {
    [login.pending]: (state) => {
      state.status = 'loading';
    },
    [login.fulfilled]: (state, action) => {
      state.status = 'succeeded';
      state.token = action.payload.access;
    },
    [login.rejected]: (state, action) => {
      state.status = 'failed';
      state.error = action.error.message;
    },
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;