import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { authService } from './services/authService';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Weather from './components/weather/Weather';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

interface PrivateRouteProps {
  children: React.ReactNode;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
  return authService.isAuthenticated() ? <>{children}</> : <Navigate to="/login" />;
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/weather"
            element={
              <PrivateRoute>
                <Weather />
              </PrivateRoute>
            }
          />
          <Route path="/" element={<Navigate to="/weather" />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
};

export default App; 