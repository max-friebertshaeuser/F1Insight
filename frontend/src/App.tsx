import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/Home";
import StandingsPage from "./pages/Standings";
import NotFoundPage from "./pages/NotFound.tsx";
import "./App.css";
import DriversPage from "./pages/Drivers.tsx"; // Ensure you have your CSS file for global styles
import Login from "./pages/Login.tsx";
import Register from "./pages/Register.tsx";

function App() {
    return (
        <Router>
            {/* Navbar is always visible */}
            <Navbar />
            {/* Main content container */}
            <main className=" bg-f1-black">
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/standings" element={<StandingsPage />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/drivers" element={<DriversPage/>} />
                    {/* Add more pages here */}
                    <Route path="*" element={<NotFoundPage />} />
                </Routes>
            </main>
        </Router>
    );
}

export default App;
