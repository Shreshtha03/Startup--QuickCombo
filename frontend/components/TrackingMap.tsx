'use client';
import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix typical Leaflet icon issues in Next.js
const iconRider = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/3202/3202926.png', // Rider icon
  iconSize: [40, 40],
  iconAnchor: [20, 20],
  popupAnchor: [0, -20],
});

const iconHome = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/2619/2619089.png', // Home/Location icon
  iconSize: [36, 36],
  iconAnchor: [18, 36],
  popupAnchor: [0, -36],
});

const iconShop = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/3081/3081840.png', // Shop icon
  iconSize: [40, 40],
  iconAnchor: [20, 40],
  popupAnchor: [0, -40],
});

interface TrackingMapProps {
  riderLat: number;
  riderLng: number;
  deliveryLat: number;
  deliveryLng: number;
  restaurantLat?: number;
  restaurantLng?: number;
}

// Map updater to smoothly pan to bounds
function MapUpdater({ bounds }: { bounds: L.LatLngBounds }) {
  const map = useMap();
  useEffect(() => {
    map.fitBounds(bounds, { padding: [40, 40], animate: true, duration: 1 });
  }, [map, bounds]);
  return null;
}

export default function TrackingMap({ riderLat, riderLng, deliveryLat, deliveryLng, restaurantLat, restaurantLng }: TrackingMapProps) {
  const [bounds, setBounds] = useState<L.LatLngBounds | null>(null);

  useEffect(() => {
    if (riderLat && riderLng && deliveryLat && deliveryLng) {
      const pts: L.LatLngTuple[] = [
        [riderLat, riderLng],
        [deliveryLat, deliveryLng]
      ];
      if (restaurantLat && restaurantLng) pts.push([restaurantLat, restaurantLng]);
      const b = new L.LatLngBounds(pts);
      setBounds(b);
    }
  }, [riderLat, riderLng, deliveryLat, deliveryLng, restaurantLat, restaurantLng]);

  // Dark mode map tiles
  const tileUrl = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
  const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>';

  if (!bounds) return null;

  return (
    <div className="w-full h-full relative">
      <MapContainer 
        bounds={bounds} 
        zoomControl={false}
        className="w-full h-full"
        style={{ background: '#0a0a0a' }}
      >
        <TileLayer url={tileUrl} attribution={attribution} />
        
        <Marker position={[deliveryLat, deliveryLng]} icon={iconHome}>
          <Popup className="qc-popup">Delivery Location</Popup>
        </Marker>
        
        {restaurantLat && restaurantLng && (
          <Marker position={[restaurantLat, restaurantLng]} icon={iconShop}>
            <Popup className="qc-popup">Restaurant</Popup>
          </Marker>
        )}
        
        {/* Animated Rider Marker */}
        <Marker position={[riderLat, riderLng]} icon={iconRider}>
          <Popup className="qc-popup">Rider is here</Popup>
        </Marker>
        
        <MapUpdater bounds={bounds} />
      </MapContainer>
      
      {/* CSS overrides for dark mode map popups */}
      <style jsx global>{`
        .leaflet-popup-content-wrapper { background: #1a1a1a; color: #fff; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; }
        .leaflet-popup-tip { background: #1a1a1a; border: 1px solid rgba(255,255,255,0.1); }
        .leaflet-container a { color: #22c55e; }
        .leaflet-control-attribution { background: rgba(0,0,0,0.5) !important; color: #666 !important; }
        
        /* Pulse animation for rider */
        .leaflet-marker-icon[src*="Rider"] {
          filter: drop-shadow(0 0 10px rgba(34, 197, 94, 0.5));
        }
      `}</style>
    </div>
  );
}
