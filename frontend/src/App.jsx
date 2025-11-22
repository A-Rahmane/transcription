import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './features/auth/pages/LoginPage';
import RegisterPage from './features/auth/pages/RegisterPage';
import MediaPage from './features/media/pages/MediaPage';
import FileDetailsPage from './features/media/pages/FileDetailsPage';

const RequireAuth = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/"
            element={
              <RequireAuth>
                <Navigate to="/media" replace />
              </RequireAuth>
            }
          />
          <Route
            path="/media"
            element={
              <RequireAuth>
                <MediaPage />
              </RequireAuth>
            }
          />
          <Route
            path="/media/:folderId"
            element={
              <RequireAuth>
                <MediaPage />
              </RequireAuth>
            }
          />
          <Route
            path="/media/files/:fileId"
            element={
              <RequireAuth>
                <FileDetailsPage />
              </RequireAuth>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
