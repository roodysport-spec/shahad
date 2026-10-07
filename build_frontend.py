import os

base_dir = r"C:\Users\USER\.gemini\antigravity\scratch\volleyball-platform\frontend"

files = {
    "package.json": """{
  "name": "volleyball-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.23.1",
    "recharts": "^2.12.7",
    "axios": "^1.7.2",
    "i18next": "^23.11.5",
    "react-i18next": "^14.1.2",
    "@headlessui/react": "^2.1.1",
    "@heroicons/react": "^2.1.3",
    "react-hot-toast": "^2.4.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.4",
    "typescript": "^5.2.2",
    "vite": "^5.2.0"
  }
}
""",
    "vite.config.ts": """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
""",
    "tailwind.config.js": """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#7c3aed', // violet-600
        secondary: '#c4b5fd', // violet-300
      }
    },
  },
  plugins: [],
}
""",
    "postcss.config.js": """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""",
    "tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
""",
    "tsconfig.node.json": """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
""",
    "index.html": """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Volleyball Analytics</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""",
    "src/index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f3f4f6;
}
""",
    "src/main.tsx": """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import './i18n'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""",
    "src/i18n/index.ts": """import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import enTranslations from './en.json';
import arTranslations from './ar.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: enTranslations },
      ar: { translation: arTranslations }
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
""",
    "src/i18n/en.json": """{
  "app_title": "Volleyball Analytics",
  "dashboard": "Dashboard",
  "players": "Players",
  "fatigue": "Fatigue",
  "injury_prediction": "Injury Prediction",
  "language": "العربية",
  "total_players": "Total Players",
  "at_risk": "Players at Risk",
  "recent_entries": "Recent Fatigue Entries",
  "welcome_msg": "Welcome to Volleyball Analytics 🏐",
  "name": "Name",
  "position": "Position",
  "age": "Age",
  "add_player": "Add Player",
  "date": "Date",
  "duration": "Duration (min)",
  "intensity": "Intensity (1-10)",
  "jumps": "Jumps",
  "spikes": "Spikes",
  "sleep": "Sleep Quality",
  "stress": "Stress Level",
  "soreness": "Muscle Soreness",
  "submit": "Submit",
  "player": "Player",
  "body_part": "Body Part",
  "prev_injury": "Previous Injury?",
  "pain_level": "Pain Level",
  "predict": "Predict Risk",
  "risk_level": "Risk Level",
  "factors": "Risk Factors",
  "recommendations": "Recommendations",
  "low": "Low",
  "medium": "Medium",
  "high": "High",
  "critical": "Critical",
  "yes": "Yes",
  "no": "No",
  "save": "Save",
  "close": "Close",
  "help_duration": "Total time spent training in minutes",
  "help_intensity": "Rate of perceived exertion (RPE) from 1-10",
  "help_jumps": "Total number of jumps during the session",
  "help_spikes": "Total number of spikes/hits during the session",
  "help_sleep": "Rate sleep quality from 1 (poor) to 10 (excellent)",
  "help_stress": "Rate current stress level from 1 (low) to 10 (high)",
  "help_soreness": "Rate muscle soreness from 1 (none) to 10 (severe)"
}
""",
    "src/i18n/ar.json": """{
  "app_title": "تحليلات الكرة الطائرة",
  "dashboard": "لوحة القيادة",
  "players": "اللاعبين",
  "fatigue": "الإرهاق",
  "injury_prediction": "توقع الإصابات",
  "language": "English",
  "total_players": "إجمالي اللاعبين",
  "at_risk": "لاعبين في خطر",
  "recent_entries": "إدخالات الإرهاق الأخيرة",
  "welcome_msg": "مرحباً بك في تحليلات الكرة الطائرة 🏐",
  "name": "الاسم",
  "position": "المركز",
  "age": "العمر",
  "add_player": "إضافة لاعب",
  "date": "التاريخ",
  "duration": "المدة (دقائق)",
  "intensity": "الشدة (1-10)",
  "jumps": "القفزات",
  "spikes": "الضربات الساحقة",
  "sleep": "جودة النوم",
  "stress": "مستوى الضغط",
  "soreness": "ألم العضلات",
  "submit": "إرسال",
  "player": "اللاعب",
  "body_part": "جزء الجسم",
  "prev_injury": "إصابة سابقة؟",
  "pain_level": "مستوى الألم",
  "predict": "توقع الخطر",
  "risk_level": "مستوى الخطر",
  "factors": "عوامل الخطر",
  "recommendations": "توصيات",
  "low": "منخفض",
  "medium": "متوسط",
  "high": "عالي",
  "critical": "حرج",
  "yes": "نعم",
  "no": "لا",
  "save": "حفظ",
  "close": "إغلاق",
  "help_duration": "إجمالي وقت التدريب بالدقائق",
  "help_intensity": "معدل الجهد المبذول من 1-10",
  "help_jumps": "إجمالي عدد القفزات خلال الجلسة",
  "help_spikes": "إجمالي عدد الضربات الساحقة خلال الجلسة",
  "help_sleep": "تقييم جودة النوم من 1 (سيئ) إلى 10 (ممتاز)",
  "help_stress": "تقييم مستوى الضغط من 1 (منخفض) إلى 10 (مرتفع)",
  "help_soreness": "تقييم ألم العضلات من 1 (بدون) إلى 10 (شديد)"
}
""",
    "src/context/LanguageContext.tsx": """import React, { createContext, useContext, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

type LanguageContextType = {
  language: string;
  toggleLanguage: () => void;
};

const LanguageContext = createContext<LanguageContextType>({ language: 'en', toggleLanguage: () => {} });

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { i18n } = useTranslation();
  const [language, setLanguage] = useState(i18n.language);

  useEffect(() => {
    document.documentElement.dir = language === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = language;
  }, [language]);

  const toggleLanguage = () => {
    const newLang = language === 'en' ? 'ar' : 'en';
    i18n.changeLanguage(newLang);
    setLanguage(newLang);
  };

  return (
    <LanguageContext.Provider value={{ language, toggleLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
""",
    "src/components/Navbar.tsx": """import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useLanguage } from '../context/LanguageContext';

export default function Navbar() {
  const { t } = useTranslation();
  const { toggleLanguage } = useLanguage();
  const location = useLocation();

  const links = [
    { path: '/', label: t('dashboard') },
    { path: '/players', label: t('players') },
    { path: '/fatigue', label: t('fatigue') },
    { path: '/injury', label: t('injury_prediction') }
  ];

  return (
    <nav className="bg-primary text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-xl font-bold flex items-center gap-2">
          🏐 <span>{t('app_title')}</span>
        </div>
        <div className="flex gap-4 items-center">
          {links.map(link => (
            <Link 
              key={link.path} 
              to={link.path}
              className={`hover:text-secondary ${location.pathname === link.path ? 'font-bold underline' : ''}`}
            >
              {link.label}
            </Link>
          ))}
          <button 
            onClick={toggleLanguage}
            className="ml-4 bg-white text-primary px-3 py-1 rounded shadow text-sm font-semibold hover:bg-gray-100"
          >
            {t('language')}
          </button>
        </div>
      </div>
    </nav>
  );
}
""",
    "src/components/HelpIcon.tsx": """import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useLanguage } from '../context/LanguageContext';

type Props = {
  helpText: { en: string; ar: string }
};

export default function HelpIcon({ helpText }: Props) {
  const [isOpen, setIsOpen] = useState(false);
  const { t } = useTranslation();
  const { language } = useLanguage();

  return (
    <div className="relative inline-block ml-1 mr-1">
      <button 
        type="button"
        onClick={() => setIsOpen(true)}
        className="w-5 h-5 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center text-xs font-bold hover:bg-gray-300"
      >
        ?
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-4 rounded shadow-lg max-w-sm w-full mx-4 relative">
            <p className="text-gray-800 mb-4">{language === 'ar' ? helpText.ar : helpText.en}</p>
            <button 
              onClick={() => setIsOpen(false)}
              className="bg-primary text-white px-4 py-2 rounded w-full hover:bg-violet-700"
            >
              {t('close')}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
""",
    "src/components/RiskBadge.tsx": """import React from 'react';
import { useTranslation } from 'react-i18next';

export default function RiskBadge({ level }: { level: string }) {
  const { t } = useTranslation();
  const colors: Record<string, string> = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    critical: 'bg-red-100 text-red-800',
  };

  return (
    <span className={`px-2 py-1 rounded text-xs font-semibold ${colors[level] || 'bg-gray-100 text-gray-800'}`}>
      {t(level)}
    </span>
  );
}
""",
    "src/components/StatCard.tsx": """import React from 'react';

export default function StatCard({ title, value, icon }: { title: string, value: string | number, icon: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex items-center gap-4">
      <div className="text-4xl">{icon}</div>
      <div>
        <h3 className="text-gray-500 text-sm font-medium">{title}</h3>
        <p className="text-2xl font-bold text-gray-800">{value}</p>
      </div>
    </div>
  );
}
""",
    "src/pages/Dashboard.tsx": """import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import StatCard from '../components/StatCard';
import RiskBadge from '../components/RiskBadge';

export default function Dashboard() {
  const { t } = useTranslation();
  const [stats, setStats] = useState({ players: 0, atRisk: 0, entries: 0 });

  useEffect(() => {
    // Mock fetch for now
    setStats({ players: 12, atRisk: 3, entries: 45 });
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">{t('welcome_msg')}</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard title={t('total_players')} value={stats.players} icon="👥" />
        <StatCard title={t('at_risk')} value={stats.atRisk} icon="⚠️" />
        <StatCard title={t('recent_entries')} value={stats.entries} icon="📊" />
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">{t('players')}</h2>
        {/* Simple table placeholder */}
        <p className="text-gray-500">Player overview table goes here...</p>
      </div>
    </div>
  );
}
""",
    "src/pages/Players.tsx": """import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';

export default function Players() {
  const { t } = useTranslation();
  const [players, setPlayers] = useState<any[]>([]);

  useEffect(() => {
    axios.get('http://localhost:8000/players/')
      .then(res => setPlayers(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">{t('players')}</h1>
        <button className="bg-primary text-white px-4 py-2 rounded hover:bg-violet-700">
          {t('add_player')}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {players.map(p => (
          <Link to={`/players/${p.id}`} key={p.id} className="block bg-white p-4 rounded shadow hover:shadow-md transition">
            <h3 className="font-bold text-lg">{p.name}</h3>
            <p className="text-gray-600">{p.position} • {p.age} yrs</p>
          </Link>
        ))}
        {players.length === 0 && <p className="text-gray-500">No players found.</p>}
      </div>
    </div>
  );
}
""",
    "src/pages/PlayerDetail.tsx": """import React from 'react';
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export default function PlayerDetail() {
  const { id } = useParams();
  const { t } = useTranslation();

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">{t('player')} #{id}</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <p>Player details go here...</p>
      </div>
    </div>
  );
}
""",
    "src/pages/FatigueEntry.tsx": """import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import toast from 'react-hot-toast';
import HelpIcon from '../components/HelpIcon';

export default function FatigueEntry() {
  const { t } = useTranslation();
  const [players, setPlayers] = useState<any[]>([]);
  
  useEffect(() => {
    axios.get('http://localhost:8000/players/')
      .then(res => setPlayers(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success('Saved!');
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">{t('fatigue')}</h1>
      
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">{t('player')}</label>
          <select className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border" required>
            <option value="">Select...</option>
            {players.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 flex items-center">
            {t('duration')} 
            <HelpIcon helpText={{en: 'Total time in minutes', ar: 'إجمالي الوقت بالدقائق'}} />
          </label>
          <input type="number" className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border" required />
        </div>

        <button type="submit" className="bg-primary text-white px-4 py-2 rounded w-full hover:bg-violet-700">
          {t('submit')}
        </button>
      </form>
    </div>
  );
}
""",
    "src/pages/InjuryPrediction.tsx": """import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import toast from 'react-hot-toast';
import RiskBadge from '../components/RiskBadge';

export default function InjuryPrediction() {
  const { t } = useTranslation();
  const [players, setPlayers] = useState<any[]>([]);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    axios.get('http://localhost:8000/players/')
      .then(res => setPlayers(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // mock result
    setResult({ risk_level: 'high', risk_score: 70, recommendations: [{en: 'Rest', ar: 'راحة'}] });
  };

  return (
    <div className="p-6 max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800 mb-6">{t('injury_prediction')}</h1>
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">{t('player')}</label>
            <select className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border" required>
              <option value="">Select...</option>
              {players.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">{t('body_part')}</label>
            <select className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border" required>
              <option value="shoulder_right">Right Shoulder</option>
              <option value="knee_right">Right Knee</option>
            </select>
          </div>
          <button type="submit" className="bg-primary text-white px-4 py-2 rounded w-full hover:bg-violet-700">
            {t('predict')}
          </button>
        </form>
      </div>

      {result && (
        <div className="bg-white p-6 rounded shadow flex flex-col items-center justify-center">
          <h2 className="text-xl font-bold mb-4">Results</h2>
          <RiskBadge level={result.risk_level} />
          <p className="text-3xl font-bold mt-4">{result.risk_score}%</p>
        </div>
      )}
    </div>
  );
}
""",
    "src/App.tsx": """import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { LanguageProvider } from './context/LanguageContext';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Players from './pages/Players';
import PlayerDetail from './pages/PlayerDetail';
import FatigueEntry from './pages/FatigueEntry';
import InjuryPrediction from './pages/InjuryPrediction';

function App() {
  return (
    <LanguageProvider>
      <Router>
        <div className="min-h-screen bg-gray-50 flex flex-col">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/players" element={<Players />} />
              <Route path="/players/:id" element={<PlayerDetail />} />
              <Route path="/fatigue" element={<FatigueEntry />} />
              <Route path="/injury" element={<InjuryPrediction />} />
            </Routes>
          </main>
          <Toaster position="bottom-right" />
        </div>
      </Router>
    </LanguageProvider>
  );
}

export default App;
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path.replace("/", os.sep))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
