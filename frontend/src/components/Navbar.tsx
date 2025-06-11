import {NavLink} from "react-router-dom";
import F1Logo from "../assets/logo.svg"; // adjust path to your F1 logo SVG

const Navbar = () => {
    const navItems = [
        {name: "Standings", path: "/standings"},
        {name: "Drivers", path: "/drivers"},
        {name: "Comparison", path: "/comparison"},
        {name: "Comparison", path: "/comparison2"}, // fix duplication if needed
        {name: "Log In", path: "/login"},
    ];

    return (
        <div className="flex flex-row justify-between bg-f1black "></div>
    );
};

export default Navbar;


// <nav className="bg-f1-black text-white px-6 py-4 flex items-center justify-between shadow-md">
//     {/* Left: Logo + Title */}
//     <div className="flex items-center gap-3">
//         <img src={F1Logo} alt="F1 Logo" className="h-6"/>
//         <span className="text-white font-formula1bold text-xl tracking-wide">Insight</span>
//     </div>
//
//     {/* Right: Navigation links */}
//     <div className="flex gap-6">
//         {navItems.map(({name, path}, index) => (
//             <NavLink
//                 key={index}
//                 to={path}
//                 className={({isActive}) =>
//                     `relative text-sm tracking-wide transition
//                ${isActive ?
//                         "text-white after:absolute after:bottom-[-2px] after:left-0 after:h-[1px] after:w-full after:bg-white after:rounded"
//                         : "text-gray-300"}`
//                 }
//             >
//                 {name}
//             </NavLink>
//         ))}
//     </div>
// </nav>