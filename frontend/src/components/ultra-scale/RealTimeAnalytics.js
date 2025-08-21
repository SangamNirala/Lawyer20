/**
 * Real-time Analytics - Live performance and usage analytics
 * Displays real-time system metrics and search analytics
 */

import React, { useState, useEffect, useMemo } from 'react';
import { 
    BarChart3, TrendingUp, TrendingDown, Activity,
    Users, Search, Clock, Database, Target,
    Zap, Globe, FileText, Eye
} from 'lucide-react';

const RealTimeAnalytics = ({ metrics, searchResults = [] }) => {
    const [timeWindow, setTimeWindow] = useState('1h'); // '1h', '24h', '7d'
    const [activeTab, setActiveTab] = useState('performance'); // 'performance', 'search', 'content'

    // Mock real-time data (in production, this would come from WebSocket or polling)
    const [realtimeData, setRealtimeData] = useState({
        currentUsers: 247,
        searchesPerMinute: 42,
        avgResponseTime: 89,
        systemLoad: 0.68,
        dataProcessed: 1247839,
        activeQueries: 15
    });

    // Update real-time data periodically
    useEffect(() => {
        const interval = setInterval(() => {
            setRealtimeData(prev => ({
                currentUsers: prev.currentUsers + Math.floor((Math.random() - 0.5) * 10),
                searchesPerMinute: Math.max(1, prev.searchesPerMinute + Math.floor((Math.random() - 0.5) * 8)),
                avgResponseTime: Math.max(10, prev.avgResponseTime + Math.floor((Math.random() - 0.5) * 20)),
                systemLoad: Math.max(0, Math.min(1, prev.systemLoad + (Math.random() - 0.5) * 0.1)),
                dataProcessed: prev.dataProcessed + Math.floor(Math.random() * 1000),
                activeQueries: Math.max(0, prev.activeQueries + Math.floor((Math.random() - 0.5) * 4))
            }));
        }, 5000); // Update every 5 seconds

        return () => clearInterval(interval);
    }, []);

    // Calculate search result analytics
    const searchAnalytics = useMemo(() => {
        if (!searchResults.length) return null;

        const jurisdictionCounts = {};
        const documentTypeCounts = {};
        const confidenceScores = [];
        let totalCitations = 0;

        searchResults.forEach(result => {
            // Jurisdiction distribution
            const jurisdiction = result.jurisdiction || 'Unknown';
            jurisdictionCounts[jurisdiction] = (jurisdictionCounts[jurisdiction] || 0) + 1;

            // Document type distribution
            const docType = result.document_type || 'Unknown';
            documentTypeCounts[docType] = (documentTypeCounts[docType] || 0) + 1;

            // Confidence scores
            if (result.confidence_score) {
                confidenceScores.push(result.confidence_score);
            }

            // Citations
            if (result.citation_count) {
                totalCitations += result.citation_count;
            }
        });

        const avgConfidence = confidenceScores.length > 0 
            ? confidenceScores.reduce((sum, score) => sum + score, 0) / confidenceScores.length
            : 0;

        return {
            jurisdictionCounts,
            documentTypeCounts,
            avgConfidence,
            totalCitations,
            resultCount: searchResults.length
        };
    }, [searchResults]);

    // Performance metrics display
    const performanceMetrics = [
        {
            label: 'System Health',
            value: `${((metrics?.operationalLevel || 0.9) * 100).toFixed(1)}%`,
            icon: <Activity className="w-5 h-5" />,
            color: 'text-green-600 bg-green-100',
            trend: 'up'
        },
        {
            label: 'Active Sources',
            value: `${metrics?.sourcesActive || 0}/${metrics?.sourcesTotal || 0}`,
            icon: <Database className="w-5 h-5" />,
            color: 'text-blue-600 bg-blue-100',
            trend: 'stable'
        },
        {
            label: 'Avg Response',
            value: `${Math.round(metrics?.responseTime || realtimeData.avgResponseTime)}ms`,
            icon: <Clock className="w-5 h-5" />,
            color: 'text-purple-600 bg-purple-100',
            trend: realtimeData.avgResponseTime < 100 ? 'up' : 'down'
        },
        {
            label: 'Success Rate',
            value: `${(metrics?.successRate || 91.7).toFixed(1)}%`,
            icon: <Target className="w-5 h-5" />,
            color: 'text-orange-600 bg-orange-100',
            trend: 'up'
        }
    ];

    // Real-time activity metrics
    const activityMetrics = [
        {
            label: 'Live Users',
            value: realtimeData.currentUsers.toLocaleString(),
            icon: <Users className="w-4 h-4" />,
            color: 'text-cyan-600'
        },
        {
            label: 'Searches/min',
            value: realtimeData.searchesPerMinute,
            icon: <Search className="w-4 h-4" />,
            color: 'text-indigo-600'
        },
        {
            label: 'Active Queries',
            value: realtimeData.activeQueries,
            icon: <Zap className="w-4 h-4" />,
            color: 'text-yellow-600'
        },
        {
            label: 'Data Processed',
            value: `${(realtimeData.dataProcessed / 1000000).toFixed(1)}M`,
            icon: <FileText className="w-4 h-4" />,
            color: 'text-pink-600'
        }
    ];

    // Get trend icon
    const getTrendIcon = (trend) => {
        switch (trend) {
            case 'up':
                return <TrendingUp className="w-4 h-4 text-green-500" />;
            case 'down':
                return <TrendingDown className="w-4 h-4 text-red-500" />;
            default:
                return <Activity className="w-4 h-4 text-gray-500" />;
        }
    };

    return (
        <div className="real-time-analytics space-y-4">
            {/* Tab Navigation */}
            <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
                {[
                    { id: 'performance', label: 'Performance' },
                    { id: 'search', label: 'Search' },
                    { id: 'content', label: 'Content' }
                ].map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex-1 py-2 px-3 text-sm font-medium rounded-md transition-colors ${
                            activeTab === tab.id
                                ? 'bg-white text-blue-600 shadow-sm'
                                : 'text-gray-600 hover:text-gray-900'
                        }`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Performance Tab */}
            {activeTab === 'performance' && (
                <div className="space-y-4">
                    {/* Main Performance Metrics */}
                    <div className="grid grid-cols-1 gap-3">
                        {performanceMetrics.map((metric, index) => (
                            <div key={index} className={`p-3 rounded-lg ${metric.color} border`}>
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center">
                                        {metric.icon}
                                        <span className="ml-2 text-sm font-medium">{metric.label}</span>
                                    </div>
                                    {getTrendIcon(metric.trend)}
                                </div>
                                <div className="text-xl font-bold mt-1">{metric.value}</div>
                            </div>
                        ))}
                    </div>

                    {/* System Load Bar */}
                    <div className="bg-white p-3 border rounded-lg">
                        <div className="flex items-center justify-between text-sm mb-2">
                            <span className="font-medium text-gray-700">System Load</span>
                            <span className="text-gray-600">{(realtimeData.systemLoad * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                                className={`h-2 rounded-full transition-all duration-500 ${
                                    realtimeData.systemLoad > 0.8 ? 'bg-red-500' :
                                    realtimeData.systemLoad > 0.6 ? 'bg-yellow-500' : 'bg-green-500'
                                }`}
                                style={{ width: `${realtimeData.systemLoad * 100}%` }}
                            ></div>
                        </div>
                    </div>
                </div>
            )}

            {/* Search Tab */}
            {activeTab === 'search' && (
                <div className="space-y-4">
                    {/* Real-time Activity */}
                    <div className="grid grid-cols-2 gap-2">
                        {activityMetrics.map((metric, index) => (
                            <div key={index} className="bg-white p-3 border rounded-lg">
                                <div className="flex items-center justify-between">
                                    <div className={`${metric.color}`}>
                                        {metric.icon}
                                    </div>
                                    <div className="text-right">
                                        <div className="text-lg font-bold text-gray-900">
                                            {metric.value}
                                        </div>
                                        <div className="text-xs text-gray-600">
                                            {metric.label}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Search Analytics */}
                    {searchAnalytics && (
                        <div className="bg-white p-3 border rounded-lg">
                            <h4 className="text-sm font-medium text-gray-700 mb-3">Current Search</h4>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span className="text-gray-600">Results Found</span>
                                    <span className="font-medium">{searchAnalytics.resultCount.toLocaleString()}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-gray-600">Avg Confidence</span>
                                    <span className="font-medium">{(searchAnalytics.avgConfidence * 100).toFixed(1)}%</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-gray-600">Total Citations</span>
                                    <span className="font-medium">{searchAnalytics.totalCitations.toLocaleString()}</span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Content Tab */}
            {activeTab === 'content' && (
                <div className="space-y-4">
                    {/* Document Distribution */}
                    {searchAnalytics && (
                        <div className="bg-white p-3 border rounded-lg">
                            <h4 className="text-sm font-medium text-gray-700 mb-3">Document Types</h4>
                            <div className="space-y-2">
                                {Object.entries(searchAnalytics.documentTypeCounts)
                                    .slice(0, 5)
                                    .map(([type, count]) => {
                                        const percentage = ((count / searchAnalytics.resultCount) * 100).toFixed(1);
                                        return (
                                            <div key={type} className="flex items-center justify-between text-sm">
                                                <span className="text-gray-600 truncate">{type}</span>
                                                <div className="flex items-center space-x-2">
                                                    <div className="w-12 bg-gray-200 rounded-full h-1.5">
                                                        <div 
                                                            className="bg-blue-500 h-1.5 rounded-full" 
                                                            style={{ width: `${percentage}%` }}
                                                        ></div>
                                                    </div>
                                                    <span className="font-medium text-xs w-8 text-right">{percentage}%</span>
                                                </div>
                                            </div>
                                        );
                                    })}
                            </div>
                        </div>
                    )}

                    {/* Global Coverage */}
                    <div className="bg-white p-3 border rounded-lg">
                        <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
                            <Globe className="w-4 h-4 mr-2" />
                            Global Coverage
                        </h4>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                            <div className="text-center p-2 bg-blue-50 rounded">
                                <div className="font-bold text-blue-600">370M+</div>
                                <div className="text-blue-700">Documents</div>
                            </div>
                            <div className="text-center p-2 bg-green-50 rounded">
                                <div className="font-bold text-green-600">200+</div>
                                <div className="text-green-700">Jurisdictions</div>
                            </div>
                            <div className="text-center p-2 bg-purple-50 rounded">
                                <div className="font-bold text-purple-600">1,600+</div>
                                <div className="text-purple-700">Sources</div>
                            </div>
                            <div className="text-center p-2 bg-orange-50 rounded">
                                <div className="font-bold text-orange-600">24/7</div>
                                <div className="text-orange-700">Monitoring</div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Live Indicator */}
            <div className="flex items-center justify-center text-xs text-gray-500">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2"></div>
                Live Analytics
            </div>
        </div>
    );
};

export default RealTimeAnalytics;