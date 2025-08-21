/**
 * Ultra-Scale Search Bar - Advanced search interface
 * Intelligent search with real-time suggestions and complex filtering
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { 
    Search, Filter, Clock, TrendingUp, Zap, Settings,
    ChevronDown, X, History, Sparkles 
} from 'lucide-react';

const UltraSearchBar = ({ 
    onSearch, 
    filters, 
    isSearching, 
    searchSuggestions = [],
    recentSearches = [],
    onClearHistory 
}) => {
    const [query, setQuery] = useState('');
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
    const [advancedFilters, setAdvancedFilters] = useState({
        dateRange: null,
        confidenceThreshold: 0.7,
        citationMinimum: 0,
        includeArchived: false,
        searchOperator: 'AND'
    });

    const searchInputRef = useRef(null);
    const suggestionsRef = useRef(null);

    // Handle search execution
    const executeSearch = useCallback(() => {
        if (query.trim()) {
            onSearch(query.trim(), advancedFilters);
            setShowSuggestions(false);
        }
    }, [query, onSearch, advancedFilters]);

    // Handle Enter key press
    const handleKeyPress = useCallback((e) => {
        if (e.key === 'Enter') {
            executeSearch();
        } else if (e.key === 'Escape') {
            setShowSuggestions(false);
        }
    }, [executeSearch]);

    // Handle suggestion selection
    const selectSuggestion = useCallback((suggestion) => {
        setQuery(suggestion);
        setShowSuggestions(false);
        setTimeout(() => {
            onSearch(suggestion, advancedFilters);
        }, 100);
    }, [onSearch, advancedFilters]);

    // Handle input focus/blur
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (suggestionsRef.current && !suggestionsRef.current.contains(event.target) &&
                searchInputRef.current && !searchInputRef.current.contains(event.target)) {
                setShowSuggestions(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    // Search operators and examples
    const searchOperators = [
        { symbol: 'AND', description: 'Both terms must appear', example: 'contract AND breach' },
        { symbol: 'OR', description: 'Either term can appear', example: 'patent OR trademark' },
        { symbol: 'NOT', description: 'Exclude term', example: 'employment NOT discrimination' },
        { symbol: '"..."', description: 'Exact phrase', example: '"due process"' },
        { symbol: '*', description: 'Wildcard', example: 'constitut*' }
    ];

    return (
        <div className="ultra-search-bar relative">
            {/* Main Search Input */}
            <div className="relative">
                <div className="flex items-center bg-white rounded-xl shadow-lg border-2 border-gray-200 focus-within:border-blue-500 transition-all duration-200">
                    {/* Search Icon */}
                    <div className="pl-4 pr-2">
                        <Search className={`w-6 h-6 ${isSearching ? 'text-blue-500 animate-pulse' : 'text-gray-400'}`} />
                    </div>

                    {/* Search Input */}
                    <input
                        ref={searchInputRef}
                        type="text"
                        value={query}
                        onChange={(e) => {
                            setQuery(e.target.value);
                            setShowSuggestions(true);
                        }}
                        onFocus={() => setShowSuggestions(true)}
                        onKeyPress={handleKeyPress}
                        placeholder="Search 370M+ legal documents... (e.g., constitutional law, contract breach, patent litigation)"
                        className="flex-1 py-4 px-2 text-lg bg-transparent border-0 outline-none placeholder-gray-400"
                        disabled={isSearching}
                    />

                    {/* Active Filters Indicator */}
                    {(filters.jurisdictions?.length > 0 || filters.documentTypes?.length > 0) && (
                        <div className="flex items-center px-2 text-sm text-blue-600 bg-blue-50 rounded-full mx-2">
                            <Filter className="w-4 h-4 mr-1" />
                            {(filters.jurisdictions?.length || 0) + (filters.documentTypes?.length || 0)} filters
                        </div>
                    )}

                    {/* Advanced Filters Toggle */}
                    <button
                        onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
                        className={`p-2 mx-1 rounded-lg hover:bg-gray-100 transition-colors ${
                            showAdvancedFilters ? 'bg-blue-100 text-blue-600' : 'text-gray-400'
                        }`}
                        title="Advanced Filters"
                    >
                        <Settings className="w-5 h-5" />
                    </button>

                    {/* Search Button */}
                    <button
                        onClick={executeSearch}
                        disabled={isSearching || !query.trim()}
                        className="m-1 px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                    >
                        {isSearching ? (
                            <div className="flex items-center">
                                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                                Searching...
                            </div>
                        ) : (
                            'Search'
                        )}
                    </button>
                </div>

                {/* Search Suggestions Dropdown */}
                {showSuggestions && (searchSuggestions.length > 0 || recentSearches.length > 0) && (
                    <div 
                        ref={suggestionsRef}
                        className="absolute top-full left-0 right-0 mt-2 bg-white rounded-lg shadow-xl border border-gray-200 z-50 max-h-96 overflow-y-auto"
                    >
                        {/* Search Suggestions */}
                        {searchSuggestions.length > 0 && (
                            <div className="p-3">
                                <div className="flex items-center text-sm font-medium text-gray-600 mb-2">
                                    <Sparkles className="w-4 h-4 mr-2" />
                                    Suggestions
                                </div>
                                {searchSuggestions.map((suggestion, index) => (
                                    <button
                                        key={index}
                                        onClick={() => selectSuggestion(suggestion)}
                                        className="w-full text-left px-3 py-2 hover:bg-gray-50 rounded-lg transition-colors text-gray-700"
                                    >
                                        <div className="flex items-center">
                                            <Search className="w-4 h-4 mr-3 text-gray-400" />
                                            {suggestion}
                                        </div>
                                    </button>
                                ))}
                            </div>
                        )}

                        {/* Recent Searches */}
                        {recentSearches.length > 0 && (
                            <div className="border-t border-gray-100 p-3">
                                <div className="flex items-center justify-between mb-2">
                                    <div className="flex items-center text-sm font-medium text-gray-600">
                                        <History className="w-4 h-4 mr-2" />
                                        Recent Searches
                                    </div>
                                    <button
                                        onClick={onClearHistory}
                                        className="text-xs text-gray-400 hover:text-gray-600 transition-colors"
                                    >
                                        Clear
                                    </button>
                                </div>
                                {recentSearches.slice(0, 5).map((search, index) => (
                                    <button
                                        key={search.id || index}
                                        onClick={() => selectSuggestion(search.query)}
                                        className="w-full text-left px-3 py-2 hover:bg-gray-50 rounded-lg transition-colors"
                                    >
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center text-gray-700">
                                                <Clock className="w-4 h-4 mr-3 text-gray-400" />
                                                {search.query}
                                            </div>
                                            <div className="text-xs text-gray-400">
                                                {search.resultCount?.toLocaleString()} results
                                            </div>
                                        </div>
                                    </button>
                                ))}
                            </div>
                        )}

                        {/* Search Operators Help */}
                        <div className="border-t border-gray-100 p-3">
                            <div className="text-sm font-medium text-gray-600 mb-2">Search Operators</div>
                            <div className="grid grid-cols-1 gap-1">
                                {searchOperators.slice(0, 3).map((op, index) => (
                                    <div key={index} className="flex items-center text-xs text-gray-500">
                                        <code className="bg-gray-100 px-2 py-1 rounded mr-2 font-mono">
                                            {op.symbol}
                                        </code>
                                        <span className="mr-2">{op.description}</span>
                                        <code className="text-gray-400">{op.example}</code>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Advanced Filters Panel */}
            {showAdvancedFilters && (
                <div className="mt-4 p-6 bg-white rounded-lg shadow-lg border border-gray-200">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-800">Advanced Search Options</h3>
                        <button
                            onClick={() => setShowAdvancedFilters(false)}
                            className="p-1 hover:bg-gray-100 rounded transition-colors"
                        >
                            <X className="w-5 h-5 text-gray-400" />
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {/* Date Range Filter */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Date Range
                            </label>
                            <select
                                value={advancedFilters.dateRange || ''}
                                onChange={(e) => setAdvancedFilters(prev => ({
                                    ...prev,
                                    dateRange: e.target.value || null
                                }))}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="">All Time</option>
                                <option value="last_year">Last Year</option>
                                <option value="last_5_years">Last 5 Years</option>
                                <option value="last_10_years">Last 10 Years</option>
                                <option value="custom">Custom Range</option>
                            </select>
                        </div>

                        {/* Confidence Threshold */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Minimum Confidence: {(advancedFilters.confidenceThreshold * 100).toFixed(0)}%
                            </label>
                            <input
                                type="range"
                                min="0"
                                max="1"
                                step="0.1"
                                value={advancedFilters.confidenceThreshold}
                                onChange={(e) => setAdvancedFilters(prev => ({
                                    ...prev,
                                    confidenceThreshold: parseFloat(e.target.value)
                                }))}
                                className="w-full"
                            />
                            <div className="flex justify-between text-xs text-gray-500 mt-1">
                                <span>0%</span>
                                <span>50%</span>
                                <span>100%</span>
                            </div>
                        </div>

                        {/* Citation Minimum */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Minimum Citations
                            </label>
                            <input
                                type="number"
                                min="0"
                                value={advancedFilters.citationMinimum}
                                onChange={(e) => setAdvancedFilters(prev => ({
                                    ...prev,
                                    citationMinimum: parseInt(e.target.value) || 0
                                }))}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="0"
                            />
                        </div>

                        {/* Search Operator */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Search Operator
                            </label>
                            <select
                                value={advancedFilters.searchOperator}
                                onChange={(e) => setAdvancedFilters(prev => ({
                                    ...prev,
                                    searchOperator: e.target.value
                                }))}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="AND">AND (All terms)</option>
                                <option value="OR">OR (Any term)</option>
                                <option value="PHRASE">PHRASE (Exact phrase)</option>
                            </select>
                        </div>

                        {/* Include Archived */}
                        <div>
                            <label className="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    checked={advancedFilters.includeArchived}
                                    onChange={(e) => setAdvancedFilters(prev => ({
                                        ...prev,
                                        includeArchived: e.target.checked
                                    }))}
                                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                                />
                                <span className="text-sm font-medium text-gray-700">
                                    Include Archived Documents
                                </span>
                            </label>
                        </div>
                    </div>

                    {/* Apply Filters Button */}
                    <div className="mt-6 flex justify-end space-x-3">
                        <button
                            onClick={() => {
                                setAdvancedFilters({
                                    dateRange: null,
                                    confidenceThreshold: 0.7,
                                    citationMinimum: 0,
                                    includeArchived: false,
                                    searchOperator: 'AND'
                                });
                            }}
                            className="px-4 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                        >
                            Reset
                        </button>
                        <button
                            onClick={() => {
                                if (query.trim()) {
                                    onSearch(query.trim(), advancedFilters);
                                }
                                setShowAdvancedFilters(false);
                            }}
                            className="px-6 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-lg transition-colors"
                        >
                            Apply Filters
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UltraSearchBar;