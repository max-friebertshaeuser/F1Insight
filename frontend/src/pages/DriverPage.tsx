import { useParams } from 'react-router-dom';

const DriverPage = () => {
    const { id } = useParams();

    return (
        <div className="min-h-screen bg-f1-black text-f1-white font-fregular p-8">
            <h1 className="text-4xl font-fbold mb-4">Driver Page</h1>
            <p className="text-lg">Driver ID: {id}</p>
            {/* You'll fetch and display actual driver data here later */}
        </div>
    );
};

export default DriverPage;
