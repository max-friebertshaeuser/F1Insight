import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/Home";
import StandingsPage from "./pages/Standings";
import NotFoundPage from "./pages/NotFound.tsx";
import "./App.css";
import DriversPage from "./pages/Drivers.tsx";
import DriverPage from "./pages/DriverPage.tsx"; // Ensure you have your CSS file for global styles
import Login from "./pages/Login.tsx";
import Register from "./pages/Register.tsx";

function App() {
    return (
        <Router>
            {/* Navbar is always visible */}
            <Navbar />
            {/* Main content container */}
            <main className=" bg-f1-black pt-16 min-h-screen text-f1-white font-fregular">
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/standings" element={<StandingsPage />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/drivers" element={<DriversPage/>} />
                    <Route path="/driver/:id" element={<DriverPage />} />
                    <Route path="*" element={<NotFoundPage />} />
                </Routes>
            </main>
            {/* !!clean coding!! */}
            <div className="h-0 w-0 overflow-hidden">
                <div className="hover:border-team-mercedes"></div>
                <div className="hover:border-team-redbull"></div>
                <div className="hover:border-team-ferrari"></div>
                <div className="hover:border-team-mclaren"></div>
                <div className="hover:border-team-astonmartin"></div>
                <div className="hover:border-team-alpine"></div>
                <div className="hover:border-team-williams"></div>
                <div className="hover:border-team-sauber"></div>
                <div className="hover:border-team-haas"></div>
                <div className="hover:border-team-racingbull"></div>
            </div>
        </Router>
    );
}

export default App;
