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
import PrivateRoute from "./types/PrivateRoute.tsx";
import BettingGame from "./pages/BettingGame.tsx";
import Logout from "./pages/Logout.tsx";

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
                    <Route path="/logout" element={<Logout />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/drivers" element={<DriversPage/>} />
                    <Route path="/bettinggame" element={<PrivateRoute><BettingGame /></PrivateRoute>} />
                    {/* Add more pages here */}
                    <Route path="/driver/:id" element={<DriverPage />} />
                    <Route path="*" element={<NotFoundPage />} />
                </Routes>
            </main>
            {/* !!clean coding!! */}
            <div className="h-0 w-0 overflow-hidden">
                <div className="hover:border-team-mercedes drop-shadow-team-mercedes text-team-mercedes"></div>
                <div className="hover:border-team-redbull drop-shadow-team-redbull text-team-redbull"></div>
                <div className="hover:border-team-ferrari drop-shadow-team-ferrari text-team-ferrari"></div>
                <div className="hover:border-team-mclaren drop-shadow-team-mclaren text-team-mclaren"></div>
                <div className="hover:border-team-astonmartin drop-shadow-team-astonmartin text-team-astonmartin"></div>
                <div className="hover:border-team-alpine drop-shadow-team-alpine text-team-alpine"></div>
                <div className="hover:border-team-williams drop-shadow-team-williams text-team-williams"></div>
                <div className="hover:border-team-alfa drop-shadow-team-alfa text-team-alfa"></div>
                <div className="hover:border-team-haas drop-shadow-team-haas text-team-haas"></div>
                <div className="hover:border-team-racingbull drop-shadow-team-racingbull text-team-racingbull"></div>
            </div>

        </Router>
    );
}

export default App;
