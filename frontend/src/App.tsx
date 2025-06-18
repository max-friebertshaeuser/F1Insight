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
import BettingGame from "./pages/BettingGame/BettingGame.tsx";
import Logout from "./pages/Logout.tsx";
import TeamsPage from "./pages/TeamsPage.tsx";
import TeamDetailPage from "./pages/TeamDetailPage.tsx";
import GroupsList from "./pages/BettingGame/GroupsList.tsx";
import CreateGroup from "./pages/BettingGame/CreateGroup.tsx";
import Bottom5After from "./pages/BettingGame/Bottom5After.tsx";
import Bottom5Before from "./pages/BettingGame/Bottom5Before.tsx";
import DeleteBet from "./pages/BettingGame/DeleteBet.tsx";
import GroupInfo from "./pages/BettingGame/GroupInfo.tsx";
import JoinGroup from "./pages/BettingGame/JoinGroup.tsx";
import SetBet from "./pages/BettingGame/SetBet.tsx";
import ShowBet from "./pages/BettingGame/ShowBet.tsx";
import UpdateBet from "./pages/BettingGame/UpdateBet.tsx";
import LeaveGroup from "./pages/BettingGame/LeaveGroup.tsx";

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
                    <Route path="/teams" element={<TeamsPage />} />
                    {/* Add more pages here */}
                    <Route path="/driver/:id" element={<DriverPage />} />
                    <Route path="/team/:id" element={<TeamDetailPage />} />
                    <Route path="*" element={<NotFoundPage />} />
                    <Route path="/groups/create" element={<CreateGroup />} />
                    <Route path="/groups/join" element={<JoinGroup />} />
                    <Route path="/groups" element={<GroupsList />} />
                    <Route path="/groups/:groupId" element={<GroupInfo />} />
                    <Route path="/bets/create" element={<SetBet />} />
                    <Route path="/bets/:race_id/show" element={<ShowBet />} />
                    <Route path="/bets/:race_id/update" element={<UpdateBet />} />
                    <Route path="/bets/:race_id/delete" element={<DeleteBet />} />
                    <Route path="/bets/bottom5-before" element={<Bottom5Before />} />
                    <Route path="/bets/bottom5-after" element={<Bottom5After />} />
                    <Route path="/groups/leave" element={<LeaveGroup />} />
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
                <div className="hover:border-team-sauber drop-shadow-team-sauber text-team-sauber"></div>
                <div className="hover:border-team-haas drop-shadow-team-haas text-team-haas"></div>
                <div className="hover:border-team-racingbull drop-shadow-team-racingbull text-team-racingbull"></div>
            </div>

        </Router>
    );
}

export default App;
