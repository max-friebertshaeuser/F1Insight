import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import "../App.css";
import logo from '../assets/logo.svg';

const navRoutes = [
    { name: 'Standings', path: '/standings' },
    { name: 'Drivers', path: '/drivers' },
    { name: 'Comparison', path: '/comparison' },
    { name: 'Log In', path: '/login' },
];

const Navbar = () => {
    const [mobileOpen, setMobileOpen] = useState(false);

    return (
        <nav className="bg-f1-black text-f1-white font-fregular py-4 px-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                    <img
                        src={logo}
                        alt="F1 Logo"
                        className="h-6"
                    />
                    <span className="text-xl font-fbold">Insight</span>
                </div>

                <div className="hidden md:flex space-x-6 text-smm">
                    {navRoutes.map((route) => (
                        <NavLink
                            key={route.name}
                            to={route.path}
                            className={({ isActive }) =>
                                `px-2 border-b-2 border-r-2 rounded-br-md transition-all duration-300 ease-in-out relative ${
                                    isActive
                                        ? 'border-f1-white'
                                        : 'border-transparent hover:border-f1-white'
                                }`
                            }
                        >
                            {route.name}
                        </NavLink>
                    ))}
                </div>

                <div className="md:hidden">
                    <button onClick={() => setMobileOpen(!mobileOpen)}>
                        {mobileOpen ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
                    </button>
                </div>
            </div>

            <div
                className={`md:hidden transition-all duration-300 ease-in-out overflow-hidden ${
                    mobileOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
                }`}
            >
                <ul className="mt-4 space-y-4 text-sm">
                    {navRoutes.map((route) => (
                        <li key={`${route.name}-mobile`}>
                            <NavLink
                                to={route.path}
                                onClick={() => setMobileOpen(false)}
                                className={({ isActive }) =>
                                    `px-2 border-b-2 border-r-2 rounded-br-md transition-all duration-300 ease-in-out block ${
                                        isActive
                                            ? 'border-f1-white'
                                            : 'border-transparent hover:border-f1-white'
                                    }`
                                }
                            >
                                {route.name}
                            </NavLink>
                        </li>
                    ))}
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;
