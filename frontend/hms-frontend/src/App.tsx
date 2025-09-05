import React, { useState, Suspense, lazy, type ReactNode } from 'react'
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AppBar, Toolbar, Typography, Button, CssBaseline, ThemeProvider, Container, IconButton, CircularProgress } from '@mui/material'
import { AuthProvider, useAuth } from './context/AuthContext'
import getMonoTheme, { MonoMode } from './theme'
import Brightness4Icon from '@mui/icons-material/Brightness4'
import Brightness7Icon from '@mui/icons-material/Brightness7'

const LoginPage = lazy(() => import('./pages/LoginPage'))
const DashboardPage = lazy(() => import('./pages/DashboardPage'))
const PatientsPage = lazy(() => import('./pages/PatientsPage'))
const AppointmentsPage = lazy(() => import('./pages/AppointmentsPage'))
const BedsPage = lazy(() => import('./pages/BedManagementPage'))
const TriagePage = lazy(() => import('./pages/TriagePage'))
const NotificationsPage = lazy(() => import('./pages/NotificationsPage'))
const AnalyticsPage = lazy(() => import('./pages/AnalyticsPage'))
const RadiologyPage = lazy(() => import('./pages/RadiologyPage'))
const FeedbackPage = lazy(() => import('./pages/FeedbackPage'))
const ConsentPage = lazy(() => import('./pages/ConsentPage'))
const AuditPage = lazy(() => import('./pages/AuditPage'))
const ERAlertsPage = lazy(() => import('./pages/ERAlertsPage'))
const OTSchedulingPage = lazy(() => import('./pages/OTSchedulingPage'))
const SuperAdminPage = lazy(() => import('./pages/SuperAdminPage'))

const queryClient = new QueryClient()

function PrivateRoute({ children }: { children: ReactNode }) {
  const token = localStorage.getItem('accessToken')
  if (!token) return <Navigate to="/login" replace />
  return <>{children}</>
}

function Shell({ children, mode, toggleMode }: { children: ReactNode, mode: MonoMode, toggleMode: () => void }) {
  const { user, logout } = useAuth()
  const isAdmin = user?.role === 'SUPER_ADMIN' || user?.role === 'HOSPITAL_ADMIN'
  const isSuper = user?.role === 'SUPER_ADMIN'
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>HMS</Typography>
          <Button color="inherit" component={Link} to="/">Dashboard</Button>
          <Button color="inherit" component={Link} to="/patients">Patients</Button>
          <Button color="inherit" component={Link} to="/appointments">Appointments</Button>
          <Button color="inherit" component={Link} to="/beds">Beds</Button>
          <Button color="inherit" component={Link} to="/triage">Triage</Button>
          <Button color="inherit" component={Link} to="/analytics">Analytics</Button>
          <Button color="inherit" component={Link} to="/radiology">Radiology</Button>
          <Button color="inherit" component={Link} to="/feedback">Feedback</Button>
          <Button color="inherit" component={Link} to="/consent">Consent</Button>
          <Button color="inherit" component={Link} to="/er-alerts">ER Alerts</Button>
          <Button color="inherit" component={Link} to="/ot-scheduling">OT</Button>
          {isAdmin && <Button color="inherit" component={Link} to="/audit">Audit</Button>}
          {isAdmin && <Button color="inherit" component={Link} to="/notifications">Notifications</Button>}
          {isSuper && <Button color="inherit" component={Link} to="/superadmin">Superadmin</Button>}
          <IconButton color="inherit" onClick={toggleMode} aria-label="Toggle theme" sx={{ ml: 1 }}>
            {mode === 'light' ? <Brightness4Icon /> : <Brightness7Icon />}
          </IconButton>
          <Button color="inherit" onClick={logout}>Logout</Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ my: 3 }}>
        {children}
      </Container>
    </>
  )
}

function App() {
  const [mode, setMode] = useState<MonoMode>('light')
  const theme = getMonoTheme(mode)
  const toggleMode = () => setMode(prev => prev === 'light' ? 'dark' : 'light')
  return (
    <AuthProvider>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <BrowserRouter>
            <Suspense fallback={<Container sx={{ py: 6, textAlign: 'center' }}><CircularProgress size={28} /></Container>}>
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><DashboardPage /></Shell></PrivateRoute>} />
                <Route path="/patients" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><PatientsPage /></Shell></PrivateRoute>} />
                <Route path="/appointments" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><AppointmentsPage /></Shell></PrivateRoute>} />
                <Route path="/beds" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><BedsPage /></Shell></PrivateRoute>} />
                <Route path="/triage" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><TriagePage /></Shell></PrivateRoute>} />
                <Route path="/analytics" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><AnalyticsPage /></Shell></PrivateRoute>} />
                <Route path="/radiology" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><RadiologyPage /></Shell></PrivateRoute>} />
                <Route path="/feedback" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><FeedbackPage /></Shell></PrivateRoute>} />
                <Route path="/consent" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><ConsentPage /></Shell></PrivateRoute>} />
                <Route path="/er-alerts" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><ERAlertsPage /></Shell></PrivateRoute>} />
                <Route path="/ot-scheduling" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><OTSchedulingPage /></Shell></PrivateRoute>} />
                <Route path="/audit" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><AuditPage /></Shell></PrivateRoute>} />
                <Route path="/notifications" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><NotificationsPage /></Shell></PrivateRoute>} />
                <Route path="/superadmin" element={<PrivateRoute><Shell mode={mode} toggleMode={toggleMode}><SuperAdminPage /></Shell></PrivateRoute>} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </Suspense>
          </BrowserRouter>
        </ThemeProvider>
      </QueryClientProvider>
    </AuthProvider>
  )
}

export default App
