/**
 * Source Health Monitor - Real-time monitoring of 1,600+ sources
 * Live dashboard component for source performance and health metrics
 */

import React, { useState, useEffect, useCallback } from 'react';
import { 
    Activity, AlertCircle, CheckCircle, Clock, 
    TrendingUp, TrendingDown, RefreshCw, Globe,
    Server, Database, Wifi 
} from 'lucide-react';
import { ultraApiService } from '../../services/ultraApiService';

const SourceHealthMonitor = () => {
    const [healthData, setHealthData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [lastUpdate, setLastUpdate] = useState(null);
    const [autoRefresh, setAutoRefresh] = useState(true);
    const [selectedRegion, setSelectedRegion] = useState('all');

    // Load source health data
    const loadHealthData = useCallback(async () => {
        try {
            setIsLoading(true);
            const data = await ultraApiService.getSourceHealth();
            setHealthData(data);
            setLastUpdate(new Date());
        } catch (error) {
            console.error('Failed to load source health:', error);
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Auto-refresh effect
    useEffect(() => {
        loadHealthData();
        
        if (autoRefresh) {
            const interval = setInterval(loadHealthData, 30000); // Refresh every 30 seconds
            return () => clearInterval(interval);
        }
    }, [loadHealthData, autoRefresh]);

    // Filter sources by region
    const filteredSources = React.useMemo(() => {
        if (!healthData?.sourceMetrics || selectedRegion === 'all') {
            return healthData?.sourceMetrics || [];
        }
        
        return healthData.sourceMetrics.filter(source => 
            source.region?.toLowerCase() === selectedRegion.toLowerCase()
        );
    }, [healthData?.sourceMetrics, selectedRegion]);

    // Calculate regional statistics
    const regionalStats = React.useMemo(() => {
        if (!healthData?.regionalSummaries) return [];
        
        return healthData.regionalSummaries.map(region => ({
            ...region,
            healthScore: (region.average_success_rate * 100).toFixed(1),
            status: region.average_success_rate > 0.8 ? 'healthy' : 
                   region.average_success_rate > 0.6 ? 'warning' : 'critical'
        }));
    }, [healthData?.regionalSummaries]);

    // Get status color and icon
    const getStatusDisplay = (status) => {
        switch (status?.toLowerCase()) {
            case 'active':
                return { 
                    color: 'text-green-600 bg-green-100', 
                    icon: <CheckCircle className="w-4 h-4" />,
                    text: 'Active'
                };
            case 'degraded':
                return { 
                    color: 'text-yellow-600 bg-yellow-100', 
                    icon: <AlertCircle className="w-4 h-4" />,
                    text: 'Degraded'
                };
            case 'error':
                return { 
                    color: 'text-red-600 bg-red-100', 
                    icon: <AlertCircle className="w-4 h-4" />,
                    text: 'Error'
                };
            case 'inactive':
                return { 
                    color: 'text-gray-600 bg-gray-100', 
                    icon: <Clock className="w-4 h-4" />,
                    text: 'Inactive'
                };
            default:
                return { 
                    color: 'text-gray-600 bg-gray-100', 
                    icon: <Clock className="w-4 h-4" />,
                    text: 'Unknown'
                };
        }
    };

    if (isLoading && !healthData) {
        return (
            <div className="source-health-monitor p-4 bg-white rounded-lg border">
                <div className="flex items-center justify-center py-8">
                    <div className="text-center">
                        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
                        <p className="text-sm text-gray-600">Loading source health data...</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="source-health-monitor">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                    <Activity className="w-5 h-5 text-blue-600 mr-2" />
                    <h3 className="font-semibold text-gray-800">Source Health</h3>
                </div>
                
                <div className="flex items-center space-x-2">
                    <button
                        onClick={() => setAutoRefresh(!autoRefresh)}
                        className={`p-1 rounded ${autoRefresh ? 'text-green-600' : 'text-gray-400'}`}
                        title={autoRefresh ? 'Auto-refresh enabled' : 'Auto-refresh disabled'}
                    >
                        <RefreshCw className={`w-4 h-4 ${autoRefresh && isLoading ? 'animate-spin' : ''}`} />
                    </button>
                    
                    <button
                        onClick={loadHealthData}
                        disabled={isLoading}
                        className="p-1 text-gray-600 hover:text-gray-800 disabled:opacity-50"
                        title="Refresh now"
                    >
                        <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
                    </button>
                </div>
            </div>

            {/* Overall Statistics */}
            <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <div className="text-sm text-blue-600 font-medium">Total Sources</div>
                            <div className="text-xl font-bold text-blue-800">
                                {healthData?.totalSources || 0}
                            </div>
                        </div>
                        <Server className="w-6 h-6 text-blue-600" />
                    </div>
                </div>

                <div className="bg-green-50 p-3 rounded-lg border border-green-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <div className="text-sm text-green-600 font-medium">Active</div>
                            <div className="text-xl font-bold text-green-800">
                                {healthData?.activeSources || 0}
                            </div>
                        </div>
                        <CheckCircle className="w-6 h-6 text-green-600" />
                    </div>
                </div>

                <div className="bg-yellow-50 p-3 rounded-lg border border-yellow-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <div className="text-sm text-yellow-600 font-medium">Success Rate</div>
                            <div className="text-xl font-bold text-yellow-800">
                                {((healthData?.overallSuccessRate || 0) * 100).toFixed(1)}%
                            </div>
                        </div>
                        <TrendingUp className="w-6 h-6 text-yellow-600" />
                    </div>
                </div>

                <div className="bg-purple-50 p-3 rounded-lg border border-purple-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <div className="text-sm text-purple-600 font-medium">Documents</div>
                            <div className="text-xl font-bold text-purple-800">
                                {((healthData?.totalDocuments || 0) / 1000000).toFixed(1)}M
                            </div>
                        </div>
                        <Database className="w-6 h-6 text-purple-600" />
                    </div>
                </div>
            </div>

            {/* Regional Health Overview */}
            {regionalStats.length > 0 && (
                <div className="mb-4">
                    <div className="text-sm font-medium text-gray-700 mb-2">Regional Health</div>
                    <div className="space-y-2">
                        {regionalStats.slice(0, 5).map((region, index) => {
                            const status = getStatusDisplay(region.status);
                            
                            return (
                                <div 
                                    key={index}
                                    className="flex items-center justify-between p-2 bg-gray-50 rounded text-sm hover:bg-gray-100 cursor-pointer transition-colors"
                                    onClick={() => setSelectedRegion(selectedRegion === region.region ? 'all' : region.region)}
                                >
                                    <div className="flex items-center">
                                        <Globe className="w-4 h-4 text-gray-500 mr-2" />
                                        <span className="font-medium">{region.region}</span>
                                        <span className="ml-2 text-gray-500">
                                            ({region.active_sources}/{region.total_sources})
                                        </span>
                                    </div>
                                    
                                    <div className="flex items-center space-x-2">
                                        <div className="text-sm font-medium text-gray-700">
                                            {region.healthScore}%
                                        </div>
                                        <div className={`px-2 py-1 rounded-full text-xs ${status.color}`}>
                                            {status.text}
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Critical Issues */}
            {healthData?.criticalIssues?.length > 0 && (
                <div className="mb-4">
                    <div className="text-sm font-medium text-red-700 mb-2">Critical Issues</div>
                    <div className="space-y-1">
                        {healthData.criticalIssues.slice(0, 3).map((issue, index) => (
                            <div key={index} className="flex items-start p-2 bg-red-50 border border-red-200 rounded text-sm">
                                <AlertCircle className="w-4 h-4 text-red-600 mr-2 mt-0.5 flex-shrink-0" />
                                <div>
                                    <div className="font-medium text-red-800">{issue.type}</div>
                                    <div className="text-red-700">{issue.message}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Performance Metrics */}
            <div className="mb-4">
                <div className="text-sm font-medium text-gray-700 mb-2">Performance</div>
                <div className="grid grid-cols-1 gap-2">
                    <div className="flex items-center justify-between p-2 bg-gray-50 rounded text-sm">
                        <span className="text-gray-600">Avg Response Time</span>
                        <span className="font-medium">
                            {(healthData?.averageResponseTimeMs || 0).toFixed(0)}ms
                        </span>
                    </div>
                    
                    <div className="flex items-center justify-between p-2 bg-gray-50 rounded text-sm">
                        <span className="text-gray-600">Documents/24h</span>
                        <span className="font-medium">
                            {(healthData?.documentsLast24h || 0).toLocaleString()}
                        </span>
                    </div>
                    
                    {healthData?.capacityMetrics?.currentThroughputDocsPerHour && (
                        <div className="flex items-center justify-between p-2 bg-gray-50 rounded text-sm">
                            <span className="text-gray-600">Current Throughput</span>
                            <span className="font-medium">
                                {healthData.capacityMetrics.currentThroughputDocsPerHour.toLocaleString()}/hr
                            </span>
                        </div>
                    )}
                </div>
            </div>

            {/* Last Update */}
            {lastUpdate && (
                <div className="text-xs text-gray-500 text-center">
                    Last updated: {lastUpdate.toLocaleTimeString()}
                </div>
            )}
        </div>
    );
};

export default SourceHealthMonitor;