'use client';
import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, ShoppingBag, Utensils, Settings, 
  TrendingUp, Clock, CheckCircle, Package, Search,
  Plus, Edit2, Trash2, ChevronRight, LogOut, Loader2
} from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const API = process.env.NEXT_PUBLIC_API_URL || 'https://quickcombo.alwaysdata.net';

export default function AdminDashboard() {
  const { user, isLoggedIn, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<any>(null);
  const [orders, setOrders] = useState<any[]>([]);
  const [menuItems, setMenuItems] = useState<any[]>([]);

  // Auth Protection
  useEffect(() => {
    if (isLoggedIn && user && !user.is_staff) {
      toast.error('Access Denied: Admins Only');
      window.location.href = '/';
    }
    if (isLoggedIn && user?.is_staff) {
      fetchData();
    }
  }, [isLoggedIn, user]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const config = { headers: { 'X-User-Email': user?.email } };
      const [sRes, oRes, mRes] = await Promise.all([
        axios.get(`${API}/api/admin/stats/`, config),
        axios.get(`${API}/api/admin/orders/`, config),
        axios.get(`${API}/api/admin/menu/`, config)
      ]);
      setStats(sRes.data);
      setOrders(oRes.data);
      setMenuItems(mRes.data);
    } catch (e) {
      toast.error('Failed to load admin data');
    } finally {
      setLoading(false);
    }
  };

  const updateOrderStatus = async (orderId: number, status: string) => {
    try {
      const config = { headers: { 'X-User-Email': user?.email } };
      await axios.patch(`${API}/api/admin/orders/`, { order_id: orderId, status }, config);
      toast.success(`Order #${orderId} set to ${status}`);
      fetchData();
    } catch (e) {
      toast.error('Update failed');
    }
  };

  if (!isLoggedIn || !user?.is_staff) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-green-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#050505] text-white flex">
      {/* --- Sidebar --- */}
      <motion.aside 
        initial={{ x: -100 }} animate={{ x: 0 }}
        className="w-64 bg-[#0a0a0a] border-r border-white/5 p-6 flex flex-col gap-8 sticky top-0 h-screen"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center shadow-[0_0_20px_#22c55e44]">
            <Utensils className="text-black w-6 h-6" />
          </div>
          <h1 className="font-black text-xl tracking-tighter">QC ADMIN</h1>
        </div>

        <nav className="flex flex-col gap-2 flex-grow">
          {[
            { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
            { id: 'orders', label: 'Orders', icon: ShoppingBag },
            { id: 'menu', label: 'Menu Items', icon: Utensils },
            { id: 'settings', label: 'Settings', icon: Settings },
          ].map(item => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                activeTab === item.id 
                ? 'bg-green-500/10 text-green-500 border border-green-500/20 shadow-[inset_0_0_15px_#22c55e11]' 
                : 'text-gray-500 hover:text-white hover:bg-white/5'
              }`}
            >
              <item.icon size={20} />
              <span className="font-semibold">{item.label}</span>
            </button>
          ))}
        </nav>

        <button 
          onClick={logout}
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-red-500 hover:bg-red-500/10 transition-all border border-transparent hover:border-red-500/20"
        >
          <LogOut size={20} />
          <span className="font-semibold">Logout</span>
        </button>
      </motion.aside>

      {/* --- Main Content --- */}
      <main className="flex-grow p-10 overflow-y-auto">
        <header className="flex justify-between items-center mb-12">
          <div>
            <h2 className="text-3xl font-bold capitalize">{activeTab}</h2>
            <p className="text-gray-500">Welcome back, {user.name || 'Admin'}</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-[#0a0a0a] border border-white/5 rounded-full px-5 py-2 flex items-center gap-3">
              <Search className="text-gray-500" size={18} />
              <input type="text" placeholder="Search anything..." className="bg-transparent border-none outline-none text-sm w-48" />
            </div>
          </div>
        </header>

        {loading ? (
          <div className="h-64 flex items-center justify-center"><Loader2 className="animate-spin text-green-500" /></div>
        ) : (
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' && (
              <motion.div 
                key="dashboard" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
                className="grid grid-cols-4 gap-6"
              >
                <StatCard label="Total Sales" value={`₹${stats?.total_sales}`} icon={TrendingUp} color="green" />
                <StatCard label="Total Orders" value={stats?.total_orders} icon={Package} color="blue" />
                <StatCard label="Pending" value={stats?.pending_orders} icon={Clock} color="orange" />
                <StatCard label="Active Status" value={stats?.active_orders} icon={CheckCircle} color="purple" />
                
                {/* Recent Orders Preview */}
                <div className="col-span-4 bg-[#0a0a0a] rounded-3xl p-8 border border-white/5 shadow-2xl mt-6">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-bold">Recent Orders</h3>
                    <button onClick={() => setActiveTab('orders')} className="text-green-500 text-sm hover:underline">View All</button>
                  </div>
                  <OrderList items={orders.slice(0, 5)} onUpdate={updateOrderStatus} />
                </div>
              </motion.div>
            )}

            {activeTab === 'orders' && (
              <motion.div 
                key="orders" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                className="bg-[#0a0a0a] rounded-3xl p-8 border border-white/5"
              >
                <OrderList items={orders} onUpdate={updateOrderStatus} />
              </motion.div>
            )}

            {activeTab === 'menu' && (
              <motion.div 
                key="menu" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                className="bg-[#0a0a0a] rounded-3xl p-8 border border-white/5"
              >
                 <div className="flex justify-between items-center mb-8">
                   <h3 className="text-xl font-bold">Manage Menu</h3>
                   <button className="bg-green-500 text-black px-5 py-2 rounded-xl font-bold flex items-center gap-2 hover:scale-105 transition-all">
                     <Plus size={18} /> Add Item
                   </button>
                 </div>
                 <div className="grid grid-cols-1 gap-4">
                   {menuItems.map(item => (
                     <div key={item.id} className="bg-white/5 rounded-2xl p-4 flex items-center justify-between group hover:bg-white/10 transition-all border border-transparent hover:border-green-500/20">
                       <div className="flex items-center gap-4">
                         <img src={item.image_url || 'https://via.placeholder.com/100'} className="w-16 h-16 rounded-xl object-cover" />
                         <div>
                           <h4 className="font-bold">{item.name}</h4>
                           <p className="text-sm text-gray-500">₹{item.price} • {item.category_name}</p>
                         </div>
                       </div>
                       <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-all">
                         <button className="p-3 bg-white/5 rounded-xl hover:text-green-500"><Edit2 size={18} /></button>
                         <button className="p-3 bg-white/5 rounded-xl hover:text-red-500"><Trash2 size={18} /></button>
                       </div>
                     </div>
                   ))}
                 </div>
              </motion.div>
            )}
          </AnimatePresence>
        )}
      </main>
    </div>
  );
}

function StatCard({ label, value, icon: Icon, color }: any) {
  const colors: any = {
    green: 'from-green-500/20 to-green-600/5 text-green-500 border-green-500/20',
    blue: 'from-blue-500/20 to-blue-600/5 text-blue-500 border-blue-500/20',
    orange: 'from-orange-500/20 to-orange-600/5 text-orange-500 border-orange-500/20',
    purple: 'from-purple-500/20 to-purple-600/5 text-purple-500 border-purple-500/20'
  };
  return (
    <div className={`bg-gradient-to-br ${colors[color]} p-6 rounded-3xl border shadow-xl`}>
      <div className="flex justify-between items-start mb-4">
        <div className="p-3 bg-black/30 rounded-2xl"><Icon size={24} /></div>
        <ChevronRight size={18} className="opacity-30" />
      </div>
      <p className="text-sm opacity-60 mb-1">{label}</p>
      <h3 className="text-3xl font-black">{value}</h3>
    </div>
  );
}

function OrderList({ items, onUpdate }: any) {
  return (
    <div className="overflow-x-auto">
      <table className="w-100 text-left border-separate border-spacing-y-3">
        <thead>
          <tr className="text-gray-500 text-sm uppercase tracking-widest">
            <th className="pb-4 px-4 font-normal">Order #</th>
            <th className="pb-4 px-4 font-normal">Customer</th>
            <th className="pb-4 px-4 font-normal">Items</th>
            <th className="pb-4 px-4 font-normal">Total</th>
            <th className="pb-4 px-4 font-normal">Status</th>
            <th className="pb-4 px-4 font-normal">Action</th>
          </tr>
        </thead>
        <tbody>
          {items.map((order: any) => (
            <tr key={order.id} className="bg-white/5 hover:bg-white/10 transition-all">
              <td className="py-4 px-4 rounded-l-2xl font-bold bg-[#111]">#{order.id}</td>
              <td className="py-4 px-4 border-y border-white/5">
                <div className="text-sm font-bold">{order.user_name || 'Guest'}</div>
                <div className="text-xs text-gray-500">{order.user_email}</div>
              </td>
              <td className="py-4 px-4 border-y border-white/5 text-sm">
                {order.items?.length || 0} items
              </td>
              <td className="py-4 px-4 border-y border-white/5 font-bold text-green-500">₹{order.total}</td>
              <td className="py-4 px-4 border-y border-white/5">
                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
                  order.status === 'pending' ? 'bg-orange-500/20 text-orange-500' :
                  order.status === 'delivered' ? 'bg-green-500/20 text-green-500' :
                  'bg-blue-500/20 text-blue-500'
                }`}>
                  {order.status}
                </span>
              </td>
              <td className="py-4 px-4 rounded-r-2xl border-y border-white/5">
                <select 
                  onChange={(e) => onUpdate(order.id, e.target.value)}
                  value={order.status}
                  className="bg-black/50 border border-white/10 rounded-lg text-xs p-1 outline-none hover:border-green-500 transition-all"
                >
                  <option value="pending">Pending</option>
                  <option value="confirmed">Confirmed</option>
                  <option value="preparing">Preparing</option>
                  <option value="picked_up">Picked Up</option>
                  <option value="out_for_delivery">Out for Delivery</option>
                  <option value="delivered">Delivered</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
