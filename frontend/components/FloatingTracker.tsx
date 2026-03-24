'use client';
import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';
import axios from 'axios';
import Link from 'next/link';
import { Bike, ChevronRight, MapPin, X } from 'lucide-react';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function FloatingTracker() {
  const [orderId, setOrderId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('');
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const checkOrder = () => {
      const saved = localStorage.getItem('activeOrderId');
      if (saved && saved !== orderId) {
        setOrderId(saved);
        fetchStatus(saved);
      }
    };

    const fetchStatus = async (id: string) => {
      try {
        const res = await axios.get(`${API}/api/orders/tracking/${id}/`);
        setStatus(res.data.label || res.data.status);
        if (res.data.status === 'delivered') {
          // Keep it for a while then remove
          setTimeout(() => {
            localStorage.removeItem('activeOrderId');
            setVisible(false);
          }, 60000);
        }
        setVisible(true);
      } catch (err) {
        setVisible(false);
      }
    };

    checkOrder();
    const interval = setInterval(() => {
        const current = localStorage.getItem('activeOrderId');
        if (current) fetchStatus(current);
        else setVisible(false);
    }, 15000);

    return () => clearInterval(interval);
  }, []);

  if (!visible || !orderId) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 100, opacity: 0 }}
        className="fixed bottom-24 left-4 right-4 z-[100] max-w-sm mx-auto"
      >
        <div className="glass-green rounded-2xl p-4 shadow-2xl border border-green-500/30 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center text-green-500">
               <Bike className="animate-bounce" size={24} />
            </div>
            <div>
              <p className="text-[10px] font-bold text-green-400 uppercase tracking-widest">Active Order #QC{orderId.padStart(4, '0')}</p>
              <h4 className="text-white font-black text-sm capitalize">{status.replace(/_/g, ' ')}...</h4>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Link href={`/orders/${orderId}`}>
                <motion.button 
                    whileTap={{ scale: 0.95 }}
                    className="bg-green-500 text-black text-[10px] font-black px-3 py-1.5 rounded-lg flex items-center gap-1"
                >
                    TRACK
                </motion.button>
            </Link>
            <button 
                onClick={() => setVisible(false)}
                className="text-gray-500 hover:text-white p-1"
            >
                <X size={16} />
            </button>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
