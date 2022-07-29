import React from "react";
import ReactDOM from "react-dom";
import CssBaseline from "@mui/material/CssBaseline";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Box } from "@mui/material";
import { SnackbarProvider } from "notistack";

<<<<<<< HEAD
//import Categories from "./pages/Categories";
//import CategoryDetails from "./pages/Categories/CategoryDetails";
=======
>>>>>>> Added-Functionality
import SignUp from "./pages/Auth/SignUp";
import SignIn from "./pages/Auth/SignIn";
import AuthContextProvider from "./contexts/AuthContextProvider";
import RequireAuth from "./components/RequireAuth";
import RequireNotAuth from "./components/RequireNotAuth";
import BaseLayout from "./components/BaseLayout";
<<<<<<< HEAD
//import Tasks from "./pages/Tasks";
//import TaskDetails from "./pages/Tasks/TaskDetails";
//import Dashboard from "./pages/Dashboard";
=======
import InLayout from "./components/InLayout";
>>>>>>> Added-Functionality
import "./index.css";
import RequestResetPassword from "./pages/Auth/RequestResetPassword";
import ResetPasswordConfirm from "./pages/Auth/ResetPasswordConfirm";
import ThemeModeProvider from "./contexts/ThemeModeProvider";
import Admin from "./pages/Admin"
<<<<<<< HEAD
=======
import SwaggerApi from "./pages/SwaggerAPI";
>>>>>>> Added-Functionality

export default function App() {
  return <ThemeModeProvider>
    <CssBaseline />


    <AuthContextProvider>
      <SnackbarProvider>
        <Router>
          <Box sx={{
            bgcolor: (theme) => theme.palette.background.default,
            minHeight: "100vh",
            width: "100%"
          }}>
            <Routes>

              {/* <Route path="/admin" element={<Admin />} />*/}
              <Route path="/doc" element={<SwaggerApi/>} /> 

              <Route element={<RequireAuth />}>
                <Route element={<BaseLayout />}>
                </Route>

              </Route>

              <Route element={<RequireNotAuth />} >
              <Route element={<InLayout />}>
                <Route path="/auth/signup" element={<SignUp />} />
                <Route path="/auth/signin" element={<SignIn />} />
                <Route path="/auth/password-reset" element={<RequestResetPassword />} />
                <Route path="/auth/password-reset/confirm/:uid/:token" element={<ResetPasswordConfirm />} />
              </Route>
              </Route>

            </Routes>
          </Box>
        </Router>
      </SnackbarProvider>
    </AuthContextProvider>

  </ThemeModeProvider>
}

ReactDOM.render(<App />, document.getElementById("root"))