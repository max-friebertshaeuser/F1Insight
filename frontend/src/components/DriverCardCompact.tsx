import type { Driver } from '../types/driver';

interface Props {
  driver: Partial<Driver>;
  label?: string;
}

export default function DriverCardCompact({ driver, label }: Props) {
  return (
    <div className="bg-gray-700 rounded-md p-2 text-center text-sm w-full">
      {label && <div className="text-xs text-gray-300 mb-1">{label}</div>}

      <img
        src={`/assets/driver-images/${driver.surname == "Verstappen" ? "max_verstappen" : driver.surname?.toLowerCase()}.avif`}
        alt={`${driver.forename} ${driver.surname}`}
        className="w-16 h-16 object-cover mx-auto rounded-full mb-1 border border-gray-500"
      />

      <div className="font-medium text-sm">
        {driver.forename} {driver.surname}
      </div>
    </div>
  );
}
