type ButtonProps = {
    active?: boolean;
    onClick?: () => void;
    children: React.ReactNode;
};

export default function Button({ active, onClick, children }: ButtonProps) {
    return (
        <button
            onClick={onClick}
            className={`border-b-2 border-r-2 rounded-br-xl text-2xl font-fwide px-8 py-2 transition-all duration-200
        ${active
                ? ' border-f1-white  text-f1-white'
                : 'text-white/60 hover:text-white border-transparent hover:border-f1-white/60'}`}
        >
            {children}
        </button>
    );
}
