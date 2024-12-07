import { useRef, useEffect, useState } from "react";
import locationsData from "./locations";

export function CreateMap() {
  const mapContainer = useRef(null); // Контейнер для карты
  const [locations, setLocations] = useState(locationsData); // Состояние для меток

  // Для хранения экземпляра карты
  const mapInstance = useRef(null);

  useEffect(() => {
    // Загрузка данных из JSON

    // Если карта уже создана, не создаем её заново
    if (mapInstance.current) return;

    const script = document.createElement("script");
    script.src =
      "https://api-maps.yandex.ru/2.1/?apikey=2fdfcc69-89ac-4cac-aeff-6d58d103a535&lang=ru_RU";
    script.async = true;
    script.onload = () => {
      if (window.ymaps) {
        window.ymaps.ready(() => {
          // Создание карты
          mapInstance.current = new window.ymaps.Map(mapContainer.current, {
            center: [56.009, 92.874], // Координаты Красноярска
            zoom: 10,
            controls: [], // Убираем все элементы управления
          });

          // Добавление меток на карту
          locations.forEach((location) => {
            const placemark = new window.ymaps.Placemark(
              location.coordinates, // Координаты
              {
                balloonContent: `
                  <div style="text-align: center;">
                    <h3>${location.title}</h3>
                    <img 
                      src="${location.image}"
                      alt="${location.title}"
                      style="text-align: center; width: auto; height: auto; margin: 10px 0;" 
                    />
                    <p>${location.description}</p>
                  </div>
                `,
              },
              {
                preset: "", // Иконка для метки
              }
            );

            mapInstance.current.geoObjects.add(placemark);
          });
        });
      }
    };

    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script); // Удаляем скрипт при размонтировании компонента
    };
  }, [locations]); // Зависимость от данных, чтобы карта обновлялась при изменении данных

  return mapContainer;
}
// const [points, setPoints] = useState([
//   // Примерная координата в Москве
// ]);

// // Добавление новой метки при клике
// const handleMapClick = (e) => {
//   const coords = e.get("coords");
//   setPoints([...points, { id: Date.now(), coords }]);
// };
// return (
//   <YMaps>
//     <div>
//       My awesome application with maps!
//       <Map
//         defaultState={{ center: [56.009, 92.874], zoom: 10 }}
//         width="100%"
//         height="500px"
//         onClick={handleMapClick}
//       >
//         {points.map((point) => (
//           <Placemark key={point.id} geometry={point.coords} />
//         ))}
//       </Map>
//     </div>
//   </YMaps>
// );
