/**
 * Jurisdiction Browser - Advanced hierarchical jurisdiction selection
 * Supports 200+ jurisdictions with intelligent grouping and search
 */

import React, { useState, useMemo, useCallback } from 'react';
import { 
    ChevronDown, ChevronRight, Globe, Search, Check, 
    MapPin, Building, Users, Scale 
} from 'lucide-react';

const JurisdictionBrowser = ({ hierarchy, selectedJurisdictions = [], onSelectionChange }) => {
    const [expandedCategories, setExpandedCategories] = useState(new Set(['United States']));
    const [searchQuery, setSearchQuery] = useState('');
    const [showSearch, setShowSearch] = useState(false);

    // Flatten hierarchy for search
    const flattenedJurisdictions = useMemo(() => {
        const flattened = [];
        
        Object.entries(hierarchy).forEach(([category, subcategories]) => {
            flattened.push({ 
                name: category, 
                type: 'category', 
                path: [category],
                icon: <Globe className="w-4 h-4" />
            });
            
            Object.entries(subcategories).forEach(([subcat, jurisdictions]) => {
                flattened.push({ 
                    name: subcat, 
                    type: 'subcategory', 
                    path: [category, subcat],
                    icon: <Building className="w-4 h-4" />
                });
                
                jurisdictions.forEach(jurisdiction => {
                    flattened.push({ 
                        name: jurisdiction, 
                        type: 'jurisdiction', 
                        path: [category, subcat, jurisdiction],
                        fullPath: `${category} > ${subcat} > ${jurisdiction}`,
                        icon: <MapPin className="w-4 h-4" />
                    });
                });
            });
        });
        
        return flattened;
    }, [hierarchy]);

    // Search filtered jurisdictions
    const searchResults = useMemo(() => {
        if (!searchQuery) return [];
        
        return flattenedJurisdictions
            .filter(item => 
                item.type === 'jurisdiction' && 
                item.name.toLowerCase().includes(searchQuery.toLowerCase())
            )
            .slice(0, 20); // Limit search results
    }, [flattenedJurisdictions, searchQuery]);

    // Toggle category expansion
    const toggleCategory = useCallback((category) => {
        setExpandedCategories(prev => {
            const newSet = new Set(prev);
            if (newSet.has(category)) {
                newSet.delete(category);
            } else {
                newSet.add(category);
            }
            return newSet;
        });
    }, []);

    // Handle jurisdiction selection
    const toggleJurisdiction = useCallback((jurisdiction) => {
        const newSelection = selectedJurisdictions.includes(jurisdiction)
            ? selectedJurisdictions.filter(j => j !== jurisdiction)
            : [...selectedJurisdictions, jurisdiction];
        
        onSelectionChange(newSelection);
    }, [selectedJurisdictions, onSelectionChange]);

    // Select all jurisdictions in a category/subcategory
    const selectAllInCategory = useCallback((category, subcategory = null) => {
        const categoryJurisdictions = subcategory 
            ? hierarchy[category][subcategory] || []
            : Object.values(hierarchy[category] || {}).flat();
        
        const allSelected = categoryJurisdictions.every(j => selectedJurisdictions.includes(j));
        
        if (allSelected) {
            // Deselect all
            const newSelection = selectedJurisdictions.filter(j => !categoryJurisdictions.includes(j));
            onSelectionChange(newSelection);
        } else {
            // Select all
            const newSelection = [...new Set([...selectedJurisdictions, ...categoryJurisdictions])];
            onSelectionChange(newSelection);
        }
    }, [hierarchy, selectedJurisdictions, onSelectionChange]);

    // Get selection stats for a category
    const getCategoryStats = useCallback((category, subcategory = null) => {
        const categoryJurisdictions = subcategory 
            ? hierarchy[category][subcategory] || []
            : Object.values(hierarchy[category] || {}).flat();
        
        const selectedCount = categoryJurisdictions.filter(j => selectedJurisdictions.includes(j)).length;
        const totalCount = categoryJurisdictions.length;
        
        return { selectedCount, totalCount, allSelected: selectedCount === totalCount };
    }, [hierarchy, selectedJurisdictions]);

    // Jurisdiction type icons
    const getJurisdictionIcon = (jurisdiction, category, subcategory) => {
        if (category === 'United States') {
            if (subcategory === 'Federal') return <Scale className="w-4 h-4 text-blue-600" />;
            if (subcategory === 'State') return <MapPin className="w-4 h-4 text-green-600" />;
            if (subcategory === 'Federal Agencies') return <Building className="w-4 h-4 text-purple-600" />;
        }
        if (category === 'European Union') {
            return <Globe className="w-4 h-4 text-blue-500" />;
        }
        if (category === 'Commonwealth') {
            return <MapPin className="w-4 h-4 text-red-500" />;
        }
        if (category === 'International Organizations') {
            return <Users className="w-4 h-4 text-indigo-600" />;
        }
        return <MapPin className="w-4 h-4 text-gray-500" />;
    };

    return (
        <div className="jurisdiction-browser">
            {/* Header with Search Toggle */}
            <div className="flex items-center justify-between mb-4">
                <div className="text-sm font-medium text-gray-600">
                    {selectedJurisdictions.length} selected
                </div>
                <button
                    onClick={() => setShowSearch(!showSearch)}
                    className="p-1 hover:bg-gray-100 rounded transition-colors"
                    title="Search Jurisdictions"
                >
                    <Search className="w-4 h-4 text-gray-500" />
                </button>
            </div>

            {/* Search Box */}
            {showSearch && (
                <div className="mb-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Search jurisdictions..."
                            className="w-full pl-10 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>
                    
                    {/* Search Results */}
                    {searchQuery && searchResults.length > 0 && (
                        <div className="mt-2 max-h-48 overflow-y-auto bg-white border border-gray-200 rounded-lg shadow-sm">
                            {searchResults.map((result, index) => (
                                <button
                                    key={index}
                                    onClick={() => toggleJurisdiction(result.name)}
                                    className="w-full px-3 py-2 text-left text-sm hover:bg-gray-50 transition-colors flex items-center justify-between"
                                >
                                    <div className="flex items-center">
                                        {result.icon}
                                        <span className="ml-2">{result.name}</span>
                                    </div>
                                    <div className="text-xs text-gray-400">{result.fullPath}</div>
                                    {selectedJurisdictions.includes(result.name) && (
                                        <Check className="w-4 h-4 text-green-600" />
                                    )}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {/* Hierarchical Browser */}
            {!searchQuery && (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                    {Object.entries(hierarchy).map(([category, subcategories]) => {
                        const isExpanded = expandedCategories.has(category);
                        const categoryStats = getCategoryStats(category);
                        
                        return (
                            <div key={category} className="border border-gray-200 rounded-lg">
                                {/* Category Header */}
                                <div className="flex items-center justify-between p-3 bg-gray-50">
                                    <button
                                        onClick={() => toggleCategory(category)}
                                        className="flex items-center flex-1 text-left"
                                    >
                                        {isExpanded ? (
                                            <ChevronDown className="w-4 h-4 mr-2 text-gray-500" />
                                        ) : (
                                            <ChevronRight className="w-4 h-4 mr-2 text-gray-500" />
                                        )}
                                        <Globe className="w-4 h-4 mr-2 text-gray-600" />
                                        <span className="font-medium text-gray-800">{category}</span>
                                        <span className="ml-2 text-xs text-gray-500">
                                            ({categoryStats.selectedCount}/{categoryStats.totalCount})
                                        </span>
                                    </button>
                                    
                                    <button
                                        onClick={() => selectAllInCategory(category)}
                                        className={`px-2 py-1 text-xs rounded transition-colors ${
                                            categoryStats.allSelected 
                                                ? 'bg-blue-100 text-blue-700 hover:bg-blue-200' 
                                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                        }`}
                                    >
                                        {categoryStats.allSelected ? 'Deselect All' : 'Select All'}
                                    </button>
                                </div>

                                {/* Subcategories */}
                                {isExpanded && (
                                    <div className="p-2 space-y-1">
                                        {Object.entries(subcategories).map(([subcategory, jurisdictions]) => {
                                            const subcatStats = getCategoryStats(category, subcategory);
                                            
                                            return (
                                                <div key={subcategory} className="border border-gray-100 rounded">
                                                    {/* Subcategory Header */}
                                                    <div className="flex items-center justify-between p-2 bg-gray-25">
                                                        <div className="flex items-center">
                                                            <Building className="w-4 h-4 mr-2 text-gray-500" />
                                                            <span className="text-sm font-medium text-gray-700">
                                                                {subcategory}
                                                            </span>
                                                            <span className="ml-2 text-xs text-gray-400">
                                                                ({subcatStats.selectedCount}/{subcatStats.totalCount})
                                                            </span>
                                                        </div>
                                                        
                                                        <button
                                                            onClick={() => selectAllInCategory(category, subcategory)}
                                                            className={`px-2 py-1 text-xs rounded transition-colors ${
                                                                subcatStats.allSelected 
                                                                    ? 'bg-blue-100 text-blue-600' 
                                                                    : 'text-gray-500 hover:bg-gray-100'
                                                            }`}
                                                        >
                                                            {subcatStats.allSelected ? 'All' : 'None'}
                                                        </button>
                                                    </div>

                                                    {/* Jurisdictions */}
                                                    <div className="p-2 space-y-1 max-h-32 overflow-y-auto">
                                                        {jurisdictions.map(jurisdiction => (
                                                            <label
                                                                key={jurisdiction}
                                                                className="flex items-center p-1 hover:bg-gray-50 rounded cursor-pointer"
                                                            >
                                                                <input
                                                                    type="checkbox"
                                                                    checked={selectedJurisdictions.includes(jurisdiction)}
                                                                    onChange={() => toggleJurisdiction(jurisdiction)}
                                                                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-2"
                                                                />
                                                                {getJurisdictionIcon(jurisdiction, category, subcategory)}
                                                                <span className="ml-2 text-sm text-gray-700">
                                                                    {jurisdiction}
                                                                </span>
                                                            </label>
                                                        ))}
                                                    </div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}

            {/* Selected Jurisdictions Summary */}
            {selectedJurisdictions.length > 0 && (
                <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <div className="text-sm font-medium text-blue-800 mb-2">
                        Selected Jurisdictions ({selectedJurisdictions.length})
                    </div>
                    <div className="flex flex-wrap gap-1">
                        {selectedJurisdictions.slice(0, 8).map(jurisdiction => (
                            <span
                                key={jurisdiction}
                                className="inline-flex items-center px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full"
                            >
                                {jurisdiction}
                                <button
                                    onClick={() => toggleJurisdiction(jurisdiction)}
                                    className="ml-1 hover:text-blue-900"
                                >
                                    ×
                                </button>
                            </span>
                        ))}
                        {selectedJurisdictions.length > 8 && (
                            <span className="text-xs text-blue-600">
                                +{selectedJurisdictions.length - 8} more
                            </span>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default JurisdictionBrowser;