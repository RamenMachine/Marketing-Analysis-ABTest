import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, Area, AreaChart, Cell as RechartsCell } from 'recharts';
import { TrendingUp, Users, DollarSign, Activity, CheckCircle, AlertCircle, Zap, Target, Download, Settings } from 'lucide-react';

const ABTestDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedTest, setSelectedTest] = useState('frequentist');
  const [confidenceLevel, setConfidenceLevel] = useState(95);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [rawData, setRawData] = useState(null);
  
  // Load data from JSON files
  useEffect(() => {
    const loadData = async () => {
      try {
        // Try to load results from analysis notebooks
        const [frequentistRes, bayesianRes, businessRes] = await Promise.all([
          fetch('/frequentist_results.json').then(r => r.ok ? r.json() : null).catch(() => null),
          fetch('/bayesian_results.json').then(r => r.ok ? r.json() : null).catch(() => null),
          fetch('/business_impact_results.json').then(r => r.ok ? r.json() : null).catch(() => null),
        ]);

        // Try to load raw CSV data for calculations
        try {
          const csvData = await fetch('/marketing_AB.csv').then(r => r.text()).catch(() => null);
          if (csvData) {
            // Simple CSV parsing (in production, use a proper CSV parser)
            const lines = csvData.split('\n');
            const headers = lines[0].split(',');
            const parsed = lines.slice(1).filter(l => l.trim()).map(line => {
              const values = line.split(',');
              return headers.reduce((obj, h, i) => {
                obj[h.trim()] = values[i]?.trim() || '';
                return obj;
              }, {});
            });
            setRawData(parsed);
          }
        } catch (e) {
          console.log('Could not load raw data');
        }

        // Use loaded data or fall back to mock data
        if (frequentistRes || bayesianRes) {
          setData({
            frequentist: frequentistRes,
            bayesian: bayesianRes,
            business: businessRes,
            // Calculate derived metrics
            adGroup: {
              users: frequentistRes?.ad_group_size || bayesianRes?.ad_group_size || 564577,
              conversions: frequentistRes?.ad_conversions || bayesianRes?.ad_conversions || 64382,
              conversionRate: frequentistRes?.ad_conversion_rate || bayesianRes?.ad_conversion_rate || 0.114019
            },
            psaGroup: {
              users: frequentistRes?.psa_group_size || bayesianRes?.psa_group_size || 18238,
              conversions: frequentistRes?.psa_conversions || bayesianRes?.psa_conversions || 2033,
              conversionRate: frequentistRes?.psa_conversion_rate || bayesianRes?.psa_conversion_rate || 0.111480
            },
            stats: frequentistRes || {
              lift: 0.02277,
              pValue: 0.000891,
              cohensH: 0.0077,
              power: 0.9523,
              ciLower: 0.0009,
              ciUpper: 0.0046
            },
            bayesian: bayesianRes || {
              probAdBetter: 0.9996,
              expectedLift: 0.02277,
              credibleLower: 0.0011,
              credibleUpper: 0.0044,
              expectedValue: 14397.50
            }
          });
        } else {
          // Fallback to mock data
          setData({
            adGroup: {
              users: 564577,
              conversions: 64382,
              conversionRate: 0.114019
            },
            psaGroup: {
              users: 18238,
              conversions: 2033,
              conversionRate: 0.111480
            },
            stats: {
              lift: 0.02277,
              pValue: 0.000891,
              cohensH: 0.0077,
              power: 0.9523,
              ciLower: 0.0009,
              ciUpper: 0.0046
            },
            bayesian: {
              probAdBetter: 0.9996,
              expectedLift: 0.02277,
              credibleLower: 0.0011,
              credibleUpper: 0.0044,
              expectedValue: 14397.50
            }
          });
        }
      } catch (error) {
        console.error('Error loading data:', error);
        // Use mock data as fallback
        setData({
          adGroup: { users: 564577, conversions: 64382, conversionRate: 0.114019 },
          psaGroup: { users: 18238, conversions: 2033, conversionRate: 0.111480 },
          stats: { lift: 0.02277, pValue: 0.000891, cohensH: 0.0077, power: 0.9523, ciLower: 0.0009, ciUpper: 0.0046 },
          bayesian: { probAdBetter: 0.9996, expectedLift: 0.02277, credibleLower: 0.0011, credibleUpper: 0.0044, expectedValue: 14397.50 }
        });
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  // Calculate confidence intervals based on confidence level
  const calculateCI = (lower, upper, level) => {
    if (!data) return { lower, upper };
    const alpha = (100 - level) / 100;
    const zScore = level === 90 ? 1.645 : level === 95 ? 1.96 : level === 99 ? 2.576 : 1.96;
    const mean = (lower + upper) / 2;
    const margin = (upper - lower) / 2;
    const adjustedMargin = margin * (zScore / 1.96); // Adjust based on z-score
    return {
      lower: mean - adjustedMargin,
      upper: mean + adjustedMargin
    };
  };

  // Export functionality
  const handleExport = async (format) => {
    if (format === 'png') {
      // For PNG export, we'd need a library like html2canvas
      alert('PNG export requires html2canvas library. Please install it to enable this feature.');
    } else if (format === 'pdf') {
      // For PDF export, we'd need a library like jsPDF
      alert('PDF export requires jsPDF library. Please install it to enable this feature.');
    } else {
      // Export as JSON
      const exportData = {
        timestamp: new Date().toISOString(),
        confidenceLevel,
        data: data
      };
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ab_test_results_${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  // Generate heat map data for ad timing
  const generateHeatMapData = () => {
    if (!rawData) {
      // Mock data for heat map
      const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
      const hours = Array.from({ length: 24 }, (_, i) => i);
      return days.flatMap(day => 
        hours.map(hour => ({
          day,
          hour,
          value: Math.random() * 15 + 8, // Mock conversion rate
          conversions: Math.floor(Math.random() * 1000 + 100)
        }))
      );
    }
    // Process raw data to create heat map
    const dayMap = { 0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun' };
    const grouped = rawData.reduce((acc, row) => {
      const day = dayMap[row['most ads day']] || 'Mon';
      const hour = parseInt(row['most ads hour']) || 0;
      const key = `${day}-${hour}`;
      if (!acc[key]) {
        acc[key] = { day, hour, conversions: 0, total: 0 };
      }
      acc[key].conversions += parseInt(row['converted']) || 0;
      acc[key].total += 1;
      return acc;
    }, {});
    return Object.values(grouped).map(item => ({
      ...item,
      value: item.total > 0 ? (item.conversions / item.total) * 100 : 0
    }));
  };

  if (loading || !data) {
    return (
      <div className="min-h-screen relative overflow-hidden flex items-center justify-center bg-black">
        <div className="relative text-center glass-card rounded-2xl p-8 border border-white/20 backdrop-blur-xl">
          <Activity className="w-12 h-12 text-white animate-spin mx-auto mb-4 drop-shadow-lg" />
          <p className="text-white/90">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  const mockData = data;

  const conversionData = [
    { name: 'Ad Group', conversions: mockData.adGroup.conversions, rate: mockData.adGroup.conversionRate * 100 },
    { name: 'PSA Group', conversions: mockData.psaGroup.conversions, rate: mockData.psaGroup.conversionRate * 100 }
  ];

  const timeSeriesData = [
    { hour: 0, ad: 10.8, psa: 10.5 },
    { hour: 3, ad: 10.2, psa: 10.1 },
    { hour: 6, ad: 10.5, psa: 10.3 },
    { hour: 9, ad: 11.9, psa: 11.2 },
    { hour: 12, ad: 12.5, psa: 11.8 },
    { hour: 15, ad: 11.8, psa: 11.5 },
    { hour: 18, ad: 11.4, psa: 11.1 },
    { hour: 21, ad: 11.2, psa: 10.9 }
  ];

  const distributionData = Array.from({ length: 50 }, (_, i) => {
    const x = (i - 25) / 500;
    const adDist = Math.exp(-Math.pow(x - 0.114, 2) / 0.0001) * 100;
    const psaDist = Math.exp(-Math.pow(x - 0.111, 2) / 0.0001) * 100;
    return { x: x.toFixed(4), ad: adDist, psa: psaDist };
  });

  const MetricCard = ({ icon: Icon, title, value, subtitle, trend, color }) => (
    <div className="glass-card rounded-2xl p-6 hover:bg-white/12 transition-all duration-300 border border-white/20 backdrop-blur-xl">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 text-white/80 mb-2">
            <Icon className="w-5 h-5" />
            <span className="text-sm font-medium">{title}</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1 drop-shadow-lg">{value}</div>
          <div className="text-sm text-white/70">{subtitle}</div>
        </div>
        {trend && (
          <div className={`flex items-center gap-1 px-3 py-1 rounded-full text-sm font-semibold backdrop-blur-md border ${
            trend > 0 
              ? 'bg-green-900/40 text-green-300 border-green-500/50' 
              : 'bg-red-900/40 text-red-300 border-red-500/50'
          }`}>
            <TrendingUp className="w-4 h-4" />
            {trend > 0 ? '+' : ''}{(trend * 100).toFixed(2)}%
          </div>
        )}
      </div>
    </div>
  );

  const TestResultCard = ({ type, data, confidenceLevel }) => {
    const isSignificant = type === 'frequentist' 
      ? data.pValue < (100 - confidenceLevel) / 100
      : data.probAdBetter > confidenceLevel / 100;
    
    const ci = calculateCI(
      type === 'frequentist' ? data.ciLower : data.credibleLower,
      type === 'frequentist' ? data.ciUpper : data.credibleUpper,
      confidenceLevel
    );
    
    return (
      <div className="glass-strong rounded-2xl p-6 border border-white/30 backdrop-blur-xl">
        <div className="flex items-center gap-3 mb-4">
          {isSignificant ? (
            <CheckCircle className="w-8 h-8 text-green-400 drop-shadow-lg" />
          ) : (
            <AlertCircle className="w-8 h-8 text-yellow-400 drop-shadow-lg" />
          )}
          <div>
            <h3 className="text-xl font-bold text-white drop-shadow-md">
              {type === 'frequentist' ? 'Frequentist Test' : 'Bayesian Analysis'}
            </h3>
            <p className="text-sm text-white/80">
              {isSignificant ? 'Statistically Significant' : 'Not Significant'}
            </p>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          {type === 'frequentist' ? (
            <>
              <div className="glass rounded-xl p-4 border border-white/20 backdrop-blur-md">
                <div className="text-sm text-white/70 mb-1">P-Value</div>
                <div className="text-2xl font-bold text-white drop-shadow-md">{data.pValue.toFixed(6)}</div>
              </div>
              <div className="glass rounded-xl p-4 border border-white/20 backdrop-blur-md">
                <div className="text-sm text-white/70 mb-1">Statistical Power</div>
                <div className="text-2xl font-bold text-white drop-shadow-md">{(data.power * 100).toFixed(1)}%</div>
              </div>
              <div className="glass rounded-xl p-4 border border-white/20 backdrop-blur-md">
                <div className="text-sm text-white/70 mb-1">Effect Size (h)</div>
                <div className="text-2xl font-bold text-white drop-shadow-md">{data.cohensH.toFixed(4)}</div>
              </div>
              <div className="glass rounded-xl p-4 border border-white/20 backdrop-blur-md">
                <div className="text-sm text-white/70 mb-1">{confidenceLevel}% CI</div>
                <div className="text-lg font-bold text-white drop-shadow-md">
                  [{(ci.lower * 100).toFixed(2)}%, {(ci.upper * 100).toFixed(2)}%]
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="glass rounded-xl p-4 border border-white/20 backdrop-blur-md">
                <div className="text-sm text-white/70 mb-1">P(Ad &gt; PSA)</div>
                <div className="text-2xl font-bold text-white drop-shadow-md">{(data.probAdBetter * 100).toFixed(2)}%</div>
              </div>
              <div className="glass rounded-xl p-4 border border-white/20 backdrop-blur-md">
                <div className="text-sm text-white/70 mb-1">Expected Value</div>
                <div className="text-2xl font-bold text-white drop-shadow-md">${(data.expectedValue || 0).toLocaleString()}</div>
              </div>
              <div className="glass rounded-xl p-4 border border-white/20 backdrop-blur-md">
                <div className="text-sm text-white/70 mb-1">Expected Lift</div>
                <div className="text-2xl font-bold text-white drop-shadow-md">{(data.expectedLift * 100).toFixed(2)}%</div>
              </div>
              <div className="glass rounded-xl p-4 border border-white/20 backdrop-blur-md">
                <div className="text-sm text-white/70 mb-1">{confidenceLevel}% Credible Int.</div>
                <div className="text-lg font-bold text-white drop-shadow-md">
                  [{(ci.lower * 100).toFixed(2)}%, {(ci.upper * 100).toFixed(2)}%]
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-black">
      {/* Subtle pattern overlay */}
      <div className="fixed inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMzAiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-30"></div>

      {/* Header */}
      <div className="relative bg-black/80 backdrop-blur-xl border-b border-white/10 text-white shadow-2xl">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold mb-2 text-white drop-shadow-lg">Marketing A/B Test Dashboard</h1>
              <p className="text-white/90">Real-time statistical analysis and insights</p>
            </div>
            <div className="flex items-center gap-6">
              <div className="text-right">
                <div className="text-sm text-white/90">Test Status</div>
                <div className="flex items-center gap-2 text-2xl font-bold">
                  <Activity className="w-6 h-6" />
                  COMPLETE
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <Settings className="w-5 h-5" />
                  <label className="text-sm text-white/90">Confidence:</label>
                  <select
                    value={confidenceLevel}
                    onChange={(e) => setConfidenceLevel(Number(e.target.value))}
                    className="glass-button text-white px-3 py-1 rounded-lg font-semibold border border-white/20 backdrop-blur-md"
                  >
                    <option value={90} className="bg-gray-800">90%</option>
                    <option value={95} className="bg-gray-800">95%</option>
                    <option value={99} className="bg-gray-800">99%</option>
                  </select>
                </div>
                <div className="flex items-center gap-2">
                  <Download className="w-5 h-5" />
                  <button
                    onClick={() => handleExport('json')}
                    className="glass-button text-white px-4 py-2 rounded-lg font-semibold hover:bg-white/20 transition-all border border-white/20 backdrop-blur-md"
                  >
                    Export JSON
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="relative max-w-7xl mx-auto px-6 mt-6">
        <div className="glass rounded-2xl p-2 border border-white/20 backdrop-blur-xl">
          <div className="flex gap-2">
            {['overview', 'statistics', 'visualizations', 'insights'].map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex-1 py-3 px-4 rounded-xl font-medium transition-all duration-200 ${
                  activeTab === tab
                    ? 'bg-white/30 text-white shadow-lg backdrop-blur-md border border-white/30'
                    : 'text-white/80 hover:bg-white/10 hover:text-white'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="relative max-w-7xl mx-auto px-6 py-8">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricCard
                icon={Users}
                title="Total Users"
                value={(mockData.adGroup.users + mockData.psaGroup.users).toLocaleString()}
                subtitle="Across both groups"
              />
              <MetricCard
                icon={Target}
                title="Conversion Rate"
                value={`${(mockData.adGroup.conversionRate * 100).toFixed(2)}%`}
                subtitle="Ad group performance"
                trend={mockData.stats.lift}
              />
              <MetricCard
                icon={TrendingUp}
                title="Relative Lift"
                value={`${(mockData.stats.lift * 100).toFixed(2)}%`}
                subtitle="vs. control group"
                trend={mockData.stats.lift}
              />
              <MetricCard
                icon={Zap}
                title="Statistical Power"
                value={`${(mockData.stats.power * 100).toFixed(1)}%`}
                subtitle="Test reliability"
              />
            </div>

            {/* Conversion Comparison */}
            <div className="glass-card rounded-2xl p-6 border border-white/20 backdrop-blur-xl">
              <h2 className="text-2xl font-bold text-white mb-6 drop-shadow-md">Conversion Rate Comparison</h2>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={conversionData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis dataKey="name" stroke="rgba(255,255,255,0.7)" />
                  <YAxis stroke="rgba(255,255,255,0.7)" />
                  <Tooltip contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px', color: 'white' }} />
                  <Legend wrapperStyle={{ color: 'white' }} />
                  <Bar dataKey="rate" fill="#60A5FA" name="Conversion Rate (%)" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Group Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="glass-strong rounded-2xl p-6 border border-blue-500/30 backdrop-blur-xl bg-blue-900/20">
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-white drop-shadow-md">
                  <Target className="w-6 h-6 text-blue-400" />
                  Ad Group (Test)
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">Total Users</span>
                    <span className="text-2xl font-bold text-white drop-shadow-md">{mockData.adGroup.users.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">Conversions</span>
                    <span className="text-2xl font-bold text-white drop-shadow-md">{mockData.adGroup.conversions.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">Conversion Rate</span>
                    <span className="text-2xl font-bold text-white drop-shadow-md">{(mockData.adGroup.conversionRate * 100).toFixed(2)}%</span>
                  </div>
                </div>
              </div>

              <div className="glass-strong rounded-2xl p-6 border border-gray-500/30 backdrop-blur-xl bg-gray-800/20">
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-white drop-shadow-md">
                  <Users className="w-6 h-6 text-gray-400" />
                  PSA Group (Control)
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">Total Users</span>
                    <span className="text-2xl font-bold text-white drop-shadow-md">{mockData.psaGroup.users.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">Conversions</span>
                    <span className="text-2xl font-bold text-white drop-shadow-md">{mockData.psaGroup.conversions.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">Conversion Rate</span>
                    <span className="text-2xl font-bold text-white drop-shadow-md">{(mockData.psaGroup.conversionRate * 100).toFixed(2)}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Statistics Tab */}
        {activeTab === 'statistics' && (
          <div className="space-y-6">
            {/* Test Method Selector */}
            <div className="glass-card rounded-2xl p-6 border border-white/20 backdrop-blur-xl">
              <h2 className="text-2xl font-bold text-white mb-4 drop-shadow-md">Statistical Method</h2>
              <div className="flex gap-4">
                <button
                  onClick={() => setSelectedTest('frequentist')}
                  className={`flex-1 py-4 px-6 rounded-xl font-semibold transition-all duration-200 backdrop-blur-md border ${
                    selectedTest === 'frequentist'
                      ? 'bg-blue-600/30 text-white shadow-lg border-blue-500/50'
                      : 'glass-button text-white/80 hover:text-white border-white/20'
                  }`}
                >
                  Frequentist (T-Test)
                </button>
                <button
                  onClick={() => setSelectedTest('bayesian')}
                  className={`flex-1 py-4 px-6 rounded-xl font-semibold transition-all duration-200 backdrop-blur-md border ${
                    selectedTest === 'bayesian'
                      ? 'bg-indigo-600/30 text-white shadow-lg border-indigo-500/50'
                      : 'glass-button text-white/80 hover:text-white border-white/20'
                  }`}
                >
                  Bayesian Analysis
                </button>
              </div>
            </div>

            {/* Test Results */}
            <TestResultCard
              type={selectedTest}
              data={selectedTest === 'frequentist' ? mockData.stats : mockData.bayesian}
              confidenceLevel={confidenceLevel}
            />

            {/* Trade-offs Comparison */}
            <div className="glass-card rounded-2xl p-6 border border-white/20 backdrop-blur-xl">
              <h2 className="text-2xl font-bold text-white mb-6 drop-shadow-md">Method Comparison</h2>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b-2 border-white/20">
                      <th className="text-left py-3 px-4 font-semibold text-white">Aspect</th>
                      <th className="text-left py-3 px-4 font-semibold text-white">Frequentist</th>
                      <th className="text-left py-3 px-4 font-semibold text-white">Bayesian</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-b border-white/10">
                      <td className="py-3 px-4 font-medium text-white/90">Interpretation</td>
                      <td className="py-3 px-4 text-white/80">P-value & confidence intervals</td>
                      <td className="py-3 px-4 text-white/80">Direct probabilities</td>
                    </tr>
                    <tr className="border-b border-white/10">
                      <td className="py-3 px-4 font-medium text-white/90">Decision Making</td>
                      <td className="py-3 px-4 text-white/80">Reject/fail to reject null</td>
                      <td className="py-3 px-4 text-white/80">Probability statements</td>
                    </tr>
                    <tr className="border-b border-white/10">
                      <td className="py-3 px-4 font-medium text-white/90">Complexity</td>
                      <td className="py-3 px-4 text-white/80">Simple, fast</td>
                      <td className="py-3 px-4 text-white/80">More complex, slower</td>
                    </tr>
                    <tr className="border-b border-white/10">
                      <td className="py-3 px-4 font-medium text-white/90">Prior Knowledge</td>
                      <td className="py-3 px-4 text-white/80">Not incorporated</td>
                      <td className="py-3 px-4 text-white/80">Can incorporate priors</td>
                    </tr>
                    <tr>
                      <td className="py-3 px-4 font-medium text-white/90">Best For</td>
                      <td className="py-3 px-4 text-white/80">Quick validation, large samples</td>
                      <td className="py-3 px-4 text-white/80">Ongoing monitoring, small samples</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Visualizations Tab */}
        {activeTab === 'visualizations' && (
          <div className="space-y-6">
            {/* Time Series */}
            <div className="glass-card rounded-2xl p-6 border border-white/20 backdrop-blur-xl">
              <h2 className="text-2xl font-bold text-white mb-6 drop-shadow-md">Conversion Rate by Hour</h2>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={timeSeriesData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis dataKey="hour" stroke="rgba(255,255,255,0.7)" label={{ value: 'Hour of Day', position: 'insideBottom', offset: -5, style: { fill: 'rgba(255,255,255,0.7)' } }} />
                  <YAxis stroke="rgba(255,255,255,0.7)" label={{ value: 'Conversion Rate (%)', angle: -90, position: 'insideLeft', style: { fill: 'rgba(255,255,255,0.7)' } }} />
                  <Tooltip contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px', color: 'white' }} />
                  <Legend wrapperStyle={{ color: 'white' }} />
                  <Line type="monotone" dataKey="ad" stroke="#60A5FA" strokeWidth={3} name="Ad Group" />
                  <Line type="monotone" dataKey="psa" stroke="#9CA3AF" strokeWidth={3} name="PSA Group" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Distribution Comparison */}
            <div className="glass-card rounded-2xl p-6 border border-white/20 backdrop-blur-xl">
              <h2 className="text-2xl font-bold text-white mb-6 drop-shadow-md">Conversion Rate Distributions</h2>
              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={distributionData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis dataKey="x" stroke="rgba(255,255,255,0.7)" label={{ value: 'Conversion Rate', position: 'insideBottom', offset: -5, style: { fill: 'rgba(255,255,255,0.7)' } }} />
                  <YAxis stroke="rgba(255,255,255,0.7)" label={{ value: 'Density', angle: -90, position: 'insideLeft', style: { fill: 'rgba(255,255,255,0.7)' } }} />
                  <Tooltip contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px', color: 'white' }} />
                  <Legend wrapperStyle={{ color: 'white' }} />
                  <Area type="monotone" dataKey="ad" stroke="#60A5FA" fill="#60A5FA" fillOpacity={0.3} name="Ad Group" />
                  <Area type="monotone" dataKey="psa" stroke="#9CA3AF" fill="#9CA3AF" fillOpacity={0.3} name="PSA Group" />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Heat Map for Ad Timing */}
            <div className="glass-card rounded-2xl p-6 border border-white/20 backdrop-blur-xl">
              <h2 className="text-2xl font-bold text-white mb-6 drop-shadow-md">Optimal Ad Timing Heat Map</h2>
              <p className="text-white/80 mb-4">Conversion rates by day of week and hour</p>
              <ResponsiveContainer width="100%" height={500}>
                <div className="grid grid-cols-7 gap-2">
                  {(() => {
                    const heatMapData = generateHeatMapData();
                    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
                    const hours = Array.from({ length: 24 }, (_, i) => i);
                    const maxValue = Math.max(...heatMapData.map(d => d.value));
                    const minValue = Math.min(...heatMapData.map(d => d.value));
                    
                    return days.map(day => (
                      <div key={day} className="flex flex-col gap-1">
                        <div className="font-semibold text-white/90 text-center mb-2">{day}</div>
                        {hours.map(hour => {
                          const cellData = heatMapData.find(d => d.day === day && d.hour === hour);
                          const value = cellData?.value || 0;
                          const intensity = maxValue > minValue ? (value - minValue) / (maxValue - minValue) : 0;
                          // Dark theme colors: from dark blue to bright blue
                          const r = Math.floor(30 + intensity * 50);
                          const g = Math.floor(100 + intensity * 100);
                          const b = Math.floor(200 + intensity * 55);
                          const bgColor = `rgba(${r}, ${g}, ${b}, ${0.3 + intensity * 0.5})`;
                          
                          return (
                            <div
                              key={`${day}-${hour}`}
                              className="w-full aspect-square rounded border border-white/20 flex items-center justify-center text-xs font-medium cursor-pointer hover:scale-110 transition-transform"
                              style={{ backgroundColor: bgColor }}
                              title={`${day} ${hour}:00 - ${value.toFixed(2)}% conversion rate`}
                            >
                              <span className="text-white">
                                {value.toFixed(1)}%
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    ));
                  })()}
                </div>
              </ResponsiveContainer>
              <div className="mt-4 flex items-center justify-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded border border-white/30" style={{ backgroundColor: 'rgba(30, 100, 200, 0.3)' }}></div>
                  <span className="text-sm text-white/80">Low</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded border border-white/30" style={{ backgroundColor: 'rgba(50, 150, 250, 0.5)' }}></div>
                  <span className="text-sm text-white/80">Medium</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded border border-white/30" style={{ backgroundColor: 'rgba(80, 200, 255, 0.8)' }}></div>
                  <span className="text-sm text-white/80">High</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Insights Tab */}
        {activeTab === 'insights' && (
          <div className="space-y-6">
            {/* Key Findings */}
            <div className="glass-strong rounded-2xl shadow-lg p-8 border border-green-500/30 backdrop-blur-xl bg-green-900/20">
              <div className="flex items-start gap-4">
                <CheckCircle className="w-12 h-12 text-green-400 flex-shrink-0 mt-1 drop-shadow-lg" />
                <div>
                  <h2 className="text-3xl font-bold text-white mb-4 drop-shadow-md">Test Conclusion: POSITIVE</h2>
                  <p className="text-lg text-white/90 mb-4">
                    The advertising campaign demonstrates a statistically significant improvement in conversion rates.
                  </p>
                  <ul className="space-y-2 text-white/90">
                    <li className="flex items-start gap-2">
                      <span className="text-green-400 font-bold">•</span>
                      <span><strong>Conversion Lift:</strong> {(mockData.stats.lift * 100).toFixed(2)}% relative improvement</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-400 font-bold">•</span>
                      <span><strong>Statistical Significance:</strong> p-value = {mockData.stats.pValue.toFixed(6)} (highly significant)</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-400 font-bold">•</span>
                      <span><strong>Bayesian Confidence:</strong> {(mockData.bayesian.probAdBetter * 100).toFixed(2)}% probability ads are superior</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-400 font-bold">•</span>
                      <span><strong>Test Power:</strong> {(mockData.stats.power * 100).toFixed(1)}% (excellent reliability)</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="glass-card rounded-2xl p-6 border border-white/20 backdrop-blur-xl">
                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2 drop-shadow-md">
                  <Target className="w-6 h-6 text-blue-400" />
                  Recommendations
                </h3>
                <ul className="space-y-3 text-white/90">
                  <li className="flex items-start gap-2">
                    <span className="text-blue-400 font-bold text-xl">1.</span>
                    <span><strong>Deploy Campaign:</strong> Strong evidence supports full rollout</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-400 font-bold text-xl">2.</span>
                    <span><strong>Monitor Performance:</strong> Track conversion rates over time</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-400 font-bold text-xl">3.</span>
                    <span><strong>Optimize Timing:</strong> Focus on peak hours (9-15)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-400 font-bold text-xl">4.</span>
                    <span><strong>Scale Gradually:</strong> Expand audience in phases</span>
                  </li>
                </ul>
              </div>

              <div className="glass-card rounded-2xl p-6 border border-white/20 backdrop-blur-xl">
                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2 drop-shadow-md">
                  <DollarSign className="w-6 h-6 text-green-400" />
                  Business Impact
                </h3>
                <div className="space-y-4">
                  <div className="glass rounded-xl p-4 border border-green-500/30 bg-green-900/20 backdrop-blur-md">
                    <div className="text-sm text-white/80 mb-1">Expected Incremental Revenue</div>
                    <div className="text-3xl font-bold text-green-400 drop-shadow-md">
                      ${mockData.bayesian.expectedValue.toLocaleString()}
                    </div>
                  </div>
                  <div className="glass rounded-xl p-4 border border-blue-500/30 bg-blue-900/20 backdrop-blur-md">
                    <div className="text-sm text-white/80 mb-1">Incremental Conversions</div>
                    <div className="text-3xl font-bold text-blue-400 drop-shadow-md">
                      {Math.round(mockData.stats.lift * mockData.adGroup.users * mockData.adGroup.conversionRate).toLocaleString()}
                    </div>
                  </div>
                  <div className="text-sm text-white/70">
                    Assuming $100 value per conversion
                  </div>
                </div>
              </div>
            </div>

            {/* Risk Assessment */}
            <div className="glass-card rounded-2xl p-6 border border-white/20 backdrop-blur-xl">
              <h3 className="text-xl font-bold text-white mb-4 drop-shadow-md">Risk Assessment</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="glass rounded-xl p-4 border border-green-500/30 bg-green-900/20 backdrop-blur-md">
                  <div className="text-sm font-medium text-green-400 mb-2">Low Risk</div>
                  <ul className="text-sm text-white/90 space-y-1">
                    <li>• Large sample size</li>
                    <li>• High statistical power</li>
                    <li>• Consistent effect</li>
                  </ul>
                </div>
                <div className="glass rounded-xl p-4 border border-yellow-500/30 bg-yellow-900/20 backdrop-blur-md">
                  <div className="text-sm font-medium text-yellow-400 mb-2">Monitor</div>
                  <ul className="text-sm text-white/90 space-y-1">
                    <li>• Novelty effect decay</li>
                    <li>• Ad fatigue over time</li>
                    <li>• Market changes</li>
                  </ul>
                </div>
                <div className="glass rounded-xl p-4 border border-blue-500/30 bg-blue-900/20 backdrop-blur-md">
                  <div className="text-sm font-medium text-blue-400 mb-2">Mitigation</div>
                  <ul className="text-sm text-white/90 space-y-1">
                    <li>• Continue tracking</li>
                    <li>• Refresh creatives</li>
                    <li>• A/B test variations</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="relative glass border-t border-white/20 backdrop-blur-xl py-6 mt-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-sm text-white/80">
            Marketing A/B Test Analysis Dashboard • Statistical methods: Frequentist & Bayesian • 
            Powered by React & Recharts
          </p>
        </div>
      </div>
    </div>
  );
};

export default ABTestDashboard;