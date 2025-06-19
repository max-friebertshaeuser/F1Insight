import DriverCard from './DriverCard';
import type { Driver } from '../types/driver';

interface Props {
  title: string;
  drivers: Driver[];
  name: string;
  selection: string[] | string;
  onSelect: (id: string) => void;
  type?: 'radio' | 'checkbox';
  limit?: number;
}

export default function ScrollableDriverSelector({
  title,
  drivers,
  name,
  selection,
  onSelect,
  type = 'radio',
  limit,
}: Props) {
  const canSelect = (id: string): boolean => {
    if (type === 'checkbox' && Array.isArray(selection)) {
      return selection.length < (limit || Infinity) || selection.includes(id);
    }
    return true;
  };

  const isSelected = (id: string): boolean => {
    return Array.isArray(selection)
      ? selection.includes(id)
      : selection === id;
  };

  // Hilfsfunktion: Nur Nachnamen übergeben
  const mapToDisplayDriver = (driver : any): Driver => {
    const parts = driver.name.split(' '); // ["Max", "Verstappen"]
    const firstName = parts.slice(0, -1).join(' '); // "Max"
    const lastName = parts.slice(-1).join(' '); // "Verstappen"
    return {
      ...driver,
      forename: firstName,
      surname: lastName,
    };
  };

  return (
    <section>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <div className="flex overflow-x-auto space-x-4 pb-2 [&_.driver-points-label]:hidden  [&_.nationality-flag]:hidden">
        {drivers.map(d => {
          const displayDriver = mapToDisplayDriver(d);
          return (
            <label
              key={d.driver_id}
              className="relative flex-shrink-0"
              onClick={e => e.stopPropagation()}
            >
              <div className="pointer-events-none">
                <DriverCard driver={displayDriver} />
              </div>
              <input
                type={type}
                name={name}
                checked={isSelected(d.driver_id)}
                onChange={() => canSelect(d.driver_id) && onSelect(d.driver_id)}
                className="absolute top-2 left-2 w-5 h-5 accent-blue-500"
                disabled={!canSelect(d.driver_id)}
              />
            </label>
          );
        })}
      </div>
    </section>
  );
}
