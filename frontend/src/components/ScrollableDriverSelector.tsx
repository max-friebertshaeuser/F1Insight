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

  const getOrder = (id: string): number | null => {
    return Array.isArray(selection) ? selection.indexOf(id) + 1 || null : null;
  };

  const mapToDisplayDriver = (driver: any): Driver => {
    const parts = driver.name.split(' ');
    const firstName = parts.slice(0, -1).join(' ');
    const lastName = parts.slice(-1).join(' ');
    return {
      ...driver,
      forename: firstName,
      surname: lastName,
    };
  };

  return (
    <section>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <div className="flex overflow-x-auto space-x-4 pb-2 [&_.driver-points-label]:hidden [&_.nationality-flag]:hidden">
        {drivers.map((d) => {
          const selected = isSelected(d.driver_id);
          const order = getOrder(d.driver_id);
          const displayDriver = mapToDisplayDriver(d);

          return (
            <div
              key={d.driver_id}
              className="relative flex-shrink-0 cursor-pointer"
              onClick={() => canSelect(d.driver_id) && onSelect(d.driver_id)}
            >
              {/* Nummer oben links bei checkbox */}
              {type === 'checkbox' && (
                <div
                  className={`absolute top-2 left-2 w-6 h-6 rounded-full text-xs font-bold flex items-center justify-center z-10 ${
                    selected
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-600 text-gray-300'
                  }`}
                >
                  {selected ? order : ''}
                </div>
              )}

              <div className="pointer-events-none">
                <DriverCard driver={displayDriver} />
              </div>

              {type === 'radio' && (
                <input
                  type="radio"
                  name={name}
                  checked={selected}
                  onChange={() => canSelect(d.driver_id) && onSelect(d.driver_id)}
                  className="absolute top-2 left-2 w-5 h-5 accent-blue-500"
                  disabled={!canSelect(d.driver_id)}
                />
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
