import { CreateMap } from "./model/create-map";
export function YandexMap() {
  return (
    <div className="flex justify-center items-center">
      <div
        className="flex justify-center text-center w-50 h-500"
        ref={CreateMap()}
      />
    </div>
  );
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
