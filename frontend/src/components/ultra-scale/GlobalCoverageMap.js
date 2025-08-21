/**
 * Global Coverage Map - Geographic visualization of legal coverage
 * Shows global reach and jurisdiction distribution
 */

import React, { useState, useMemo } from 'react';
import { 
    Globe, MapPin, BarChart3, Filter,
    Layers, Eye, TrendingUp 
} from 'lucide-react';

const GlobalCoverageMap = ({ jurisdictions = [], searchResults = [] }) => {
    const [viewMode, setViewMode] = useState('coverage'); // 'coverage', 'activity', 'distribution'
    const [selectedRegion, setSelectedRegion] = useState(null);

    // Regional mapping and coverage data
    const regionData = useMemo(() => {
        const regions = {
            'North America': {
                countries: ['United States', 'Canada', 'Mexico'],
                coordinates: { x: 25, y: 35 },
                color: '#3B82F6',
                coverage: 0.95,
                sources: 450,
                documents: 125000000
            },
            'Europe': {
                countries: ['Germany', 'France', 'Italy', 'United Kingdom', 'Spain'],
                coordinates: { x: 50, y: 25 },
                color: '#10B981',
                coverage: 0.88,
                sources: 320,
                documents: 89000000
            },
            'Commonwealth': {
                countries: ['United Kingdom', 'Australia', 'Canada', 'New Zealand'],
                coordinates: { x: 75, y: 45 },
                color: '#F59E0B',
                coverage: 0.82,
                sources: 180,
                documents: 45000000
            },
            'Asia Pacific': {
                countries: ['Japan', 'South Korea', 'Singapore', 'Hong Kong'],
                coordinates: { x: 75, y: 40 },
                color: '#8B5CF6',
                coverage: 0.65,
                sources: 150,
                documents: 32000000
            },
            'International': {
                countries: ['International Organizations', 'Global Treaties'],
                coordinates: { x: 50, y: 15 },
                color: '#06B6D4',
                coverage: 0.75,
                sources: 95,
                documents: 15000000
            }
        };

        return regions;
    }, []);

    // Calculate jurisdiction activity from search results
    const jurisdictionActivity = useMemo(() => {
        if (!searchResults.length) return {};

        const activity = {};
        searchResults.forEach(result => {
            const jurisdiction = result.jurisdiction || 'Unknown';
            activity[jurisdiction] = (activity[jurisdiction] || 0) + 1;
        });

        return activity;
    }, [searchResults]);

    // Get region statistics
    const getRegionStats = () => {
        const totalSources = Object.values(regionData).reduce((sum, region) => sum + region.sources, 0);
        const totalDocuments = Object.values(regionData).reduce((sum, region) => sum + region.documents, 0);
        const avgCoverage = Object.values(regionData).reduce((sum, region) => sum + region.coverage, 0) / Object.keys(regionData).length;

        return { totalSources, totalDocuments, avgCoverage };
    };

    const stats = getRegionStats();

    // Simple world map representation using CSS and SVG-like elements
    const WorldMapVisualization = () => (
        <div className="relative w-full h-32 bg-gradient-to-b from-blue-100 to-blue-50 rounded-lg border overflow-hidden">
            {/* Continents (simplified representation) */}
            <div className="absolute inset-0">
                {/* North America */}
                <div 
                    className="absolute w-16 h-12 bg-green-200 rounded-lg transform -rotate-12"
                    style={{ left: '15%', top: '25%' }}
                />
                
                {/* Europe */}
                <div 
                    className="absolute w-8 h-6 bg-blue-200 rounded"
                    style={{ left: '47%', top: '20%' }}
                />
                
                {/* Asia */}
                <div 
                    className="absolute w-20 h-14 bg-yellow-200 rounded-lg"
                    style={{ left: '55%', top: '30%' }}
                />
                
                {/* Africa */}
                <div 
                    className="absolute w-10 h-16 bg-orange-200 rounded-lg"
                    style={{ left: '45%', top: '45%' }}
                />
                
                {/* Australia */}
                <div 
                    className="absolute w-6 h-4 bg-purple-200 rounded"
                    style={{ left: '70%', top: '65%' }}
                />
            </div>

            {/* Coverage Points */}
            {Object.entries(regionData).map(([region, data]) => (
                <div
                    key={region}
                    className={`absolute w-3 h-3 rounded-full cursor-pointer hover:scale-150 transition-transform ${
                        selectedRegion === region ? 'ring-2 ring-white animate-pulse' : ''
                    }`}
                    style={{
                        left: `${data.coordinates.x}%`,
                        top: `${data.coordinates.y}%`,
                        backgroundColor: data.color,
                        opacity: 0.8 + (data.coverage * 0.2)
                    }}
                    onClick={() => setSelectedRegion(selectedRegion === region ? null : region)}
                    title={`${region}: ${(data.coverage * 100).toFixed(0)}% coverage`}
                />
            ))}

            {/* Activity Indicators */}
            {viewMode === 'activity' && Object.entries(jurisdictionActivity).slice(0, 5).map(([jurisdiction, count], index) => {
                const region = Object.entries(regionData).find(([_, data]) => 
                    data.countries.some(country => jurisdiction.includes(country))
                );
                
                if (!region) return null;
                
                const [regionName, regionData] = region;
                return (
                    <div
                        key={jurisdiction}
                        className="absolute animate-ping"
                        style={{
                            left: `${regionData.coordinates.x + (index * 2)}%`,
                            top: `${regionData.coordinates.y + (index * 2)}%`
                        }}
                    >
                        <div className="w-2 h-2 bg-red-500 rounded-full opacity-75"></div>
                    </div>
                );
            })}
        </div>
    );

    return (
        <div className="global-coverage-map">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                    <Globe className="w-4 h-4 text-gray-600" />
                    <span className="text-sm font-medium">Global Coverage</span>
                </div>
                
                <div className="flex items-center space-x-1">
                    <button
                        onClick={() => setViewMode(viewMode === 'coverage' ? 'activity' : 'coverage')}
                        className={`p-1 rounded text-xs ${
                            viewMode === 'activity' 
                                ? 'bg-red-100 text-red-600' 
                                : 'hover:bg-gray-100 text-gray-500'
                        }`}
                        title="Toggle activity view"
                    >
                        <TrendingUp className="w-3 h-3" />
                    </button>
                </div>
            </div>

            {/* World Map */}
            <WorldMapVisualization />

            {/* Global Statistics */}
            <div className="mt-4 grid grid-cols-3 gap-2 text-xs">
                <div className="bg-blue-50 p-2 rounded text-center">
                    <div className="font-medium text-blue-800">Sources</div>
                    <div className="text-blue-600">{stats.totalSources.toLocaleString()}</div>
                </div>
                <div className="bg-green-50 p-2 rounded text-center">
                    <div className="font-medium text-green-800">Documents</div>
                    <div className="text-green-600">{(stats.totalDocuments / 1000000).toFixed(0)}M</div>
                </div>
                <div className="bg-purple-50 p-2 rounded text-center">
                    <div className="font-medium text-purple-800">Coverage</div>
                    <div className="text-purple-600">{(stats.avgCoverage * 100).toFixed(0)}%</div>
                </div>
            </div>

            {/* Regional Breakdown */}
            <div className="mt-4 space-y-2">
                <div className="text-xs font-medium text-gray-700 mb-2">Regional Coverage</div>
                {Object.entries(regionData).map(([region, data]) => (
                    <div 
                        key={region}
                        className={`flex items-center justify-between p-2 rounded text-xs cursor-pointer transition-colors ${
                            selectedRegion === region 
                                ? 'bg-gray-100 border border-gray-300' 
                                : 'hover:bg-gray-50'
                        }`}
                        onClick={() => setSelectedRegion(selectedRegion === region ? null : region)}
                    >
                        <div className="flex items-center space-x-2">
                            <div 
                                className="w-3 h-3 rounded-full"
                                style={{ backgroundColor: data.color }}
                            />
                            <span className="font-medium text-gray-700">{region}</span>
                        </div>
                        
                        <div className="flex items-center space-x-3 text-gray-500">
                            <span>{(data.coverage * 100).toFixed(0)}%</span>
                            <span>{data.sources} sources</span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Selected Region Details */}
            {selectedRegion && regionData[selectedRegion] && (
                <div className="mt-4 p-3 bg-gray-50 border rounded-lg">
                    <div className="text-sm font-medium text-gray-800 mb-2">
                        {selectedRegion}
                    </div>
                    <div className="space-y-1 text-xs text-gray-600">
                        <div className="flex justify-between">
                            <span>Coverage:</span>
                            <span className="font-medium">{(regionData[selectedRegion].coverage * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                            <span>Sources:</span>
                            <span className="font-medium">{regionData[selectedRegion].sources.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between">
                            <span>Documents:</span>
                            <span className="font-medium">{(regionData[selectedRegion].documents / 1000000).toFixed(1)}M</span>
                        </div>
                    </div>
                    
                    {/* Countries in region */}
                    <div className="mt-2">
                        <div className="text-xs text-gray-500 mb-1">Key Jurisdictions:</div>
                        <div className="flex flex-wrap gap-1">
                            {regionData[selectedRegion].countries.slice(0, 3).map(country => (
                                <span 
                                    key={country}
                                    className="px-2 py-1 bg-white text-xs rounded border"
                                >
                                    {country}
                                </span>
                            ))}
                            {regionData[selectedRegion].countries.length > 3 && (
                                <span className="px-2 py-1 bg-white text-xs rounded border text-gray-500">
                                    +{regionData[selectedRegion].countries.length - 3}
                                </span>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Current Search Activity */}
            {searchResults.length > 0 && (
                <div className="mt-4 p-2 bg-yellow-50 border border-yellow-200 rounded">
                    <div className="text-xs font-medium text-yellow-800 mb-1">
                        Current Search Activity
                    </div>
                    <div className="text-xs text-yellow-700">
                        {Object.keys(jurisdictionActivity).length} jurisdictions found with {searchResults.length} results
                    </div>
                </div>
            )}
        </div>
    );
};

export default GlobalCoverageMap;