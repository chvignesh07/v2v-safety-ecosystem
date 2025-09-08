import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, AppBar, Toolbar, Typography, Container, Box } from '@mui/material';
import { Provider } from 'react-redux';

// Import views
import DriverView from './views/DriverView';
import FleetManagerView from './views/FleetManagerView';
import EmergencyResponderView from './views/EmergencyResponderView';

// Import components
import Navigation from './components/Navigation';
import ChatPopup from './components/ChatPopup';

// Import store
import store from './store';

// Bosch-inspired theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#0074D9', // Bosch blue
      light: '#4A90E2',
      dark: '#001F3F',
    },
    secondary: {
      main: '#FF6B6B',
      light: '#FF8E8E',
      dark: '#CC5555',
    },
    background: {
      default: '#F5F7FA',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#2C3E50',
      secondary: '#6C7B7F',
    },
  },
  typography: {
    fontFamily: 'Roboto, -apple-system, BlinkMacSystemFont, sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
      color: '#2C3E50',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
      color: '#2C3E50',
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#0074D9',
          boxShadow: '0 2px 8px rgba(0,116,217,0.15)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

function App() {
  const [currentView, setCurrentView] = useState('driver'); // Default to driver view
  const [isConnected, setIsConnected] = useState(false);

  // Simulate connection status
  useEffect(() => {
    const timer = setTimeout(() => setIsConnected(true), 2000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Box sx={{ flexGrow: 1 }}>
            {/* Main App Bar */}
            <AppBar position="static">
              <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                  V2V Safety Ecosystem
                </Typography>
                <Box sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: 2,
                  color: isConnected ? '#4CAF50' : '#FF9800'
                }}>
                  <Box sx={{ 
                    width: 8, 
                    height: 8, 
                    borderRadius: '50%', 
                    backgroundColor: isConnected ? '#4CAF50' : '#FF9800'
                  }} />
                  <Typography variant="body2">
                    {isConnected ? 'Connected' : 'Connecting...'}
                  </Typography>
                </Box>
              </Toolbar>
            </AppBar>

            {/* Navigation */}
            <Navigation currentView={currentView} setCurrentView={setCurrentView} />

            {/* Main Content */}
            <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
              <Routes>
                <Route path="/" element={<Navigate to="/driver" replace />} />
                <Route path="/driver" element={<DriverView />} />
                <Route path="/fleet" element={<FleetManagerView />} />
                <Route path="/emergency" element={<EmergencyResponderView />} />
              </Routes>
            </Container>

            {/* Chat Popup */}
            <ChatPopup />
            
            {/* Footer */}
            <Box 
              component="footer" 
              sx={{ 
                mt: 'auto', 
                py: 2, 
                px: 3, 
                backgroundColor: '#2C3E50',
                color: 'white',
                textAlign: 'center'
              }}
            >
              <Typography variant="body2">
                © 2025 V2V Safety Ecosystem - Powered by Bosch Technology
              </Typography>
            </Box>
          </Box>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App;
