/**
 * Ultra-Comprehensive Legal Research Application - Step 5.1
 * Advanced frontend for 370M+ documents, 1,000+ sources, 200+ jurisdictions
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Search, Filter, BarChart3, Globe, TrendingUp, Activity } from 'lucide-react';

// Ultra-scale components
import JurisdictionBrowser from './JurisdictionBrowser';
import DocumentTypeFilter from './DocumentTypeFilter';
import SourceHealthMonitor from './SourceHealthMonitor';
import UltraSearchBar from './UltraSearchBar';
import SearchResults from './SearchResults';
import RealTimeAnalytics from './RealTimeAnalytics';
import CitationNetworkVisualization from './CitationNetworkVisualization';
import GlobalCoverageMap from './GlobalCoverageMap';

// Hooks and services
import { useUltraSearch } from '../../hooks/useUltraSearch';
import { ultraApiService } from '../../services/ultraApiService';

const UltraLegalSearchApp = () => {
    // Core state management
    const [searchResults, setSearchResults] = useState([]);
    const [totalDocuments, setTotalDocuments] = useState(370000000);
    const [isSearching, setIsSearching] = useState(false);
    const [searchError, setSearchError] = useState(null);
    
    // Advanced filter state
    const [activeFilters, setActiveFilters] = useState({
        jurisdictions: [],
        documentTypes: [],
        sources: [],
        dateRange: null,
        legalTopics: [],
        courts: [],
        qualityFilter: {
            minConfidence: 0.7,
            minCitations: 0
        }
    });

    // UI state
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const [analyticsExpanded, setAnalyticsExpanded] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const [resultsPerPage, setResultsPerPage] = useState(50);

    // System status
    const [systemStatus, setSystemStatus] = useState({
        operationalLevel: 0,
        activeSources: 0,
        totalSources: 0,
        lastUpdate: null
    });

    // Ultra-scale custom hook for search functionality
    const {
        performSearch,
        searchMetrics,
        searchSuggestions,
        recentSearches,
        clearSearchHistory
    } = useUltraSearch();

    // Comprehensive jurisdiction hierarchy with all 200+ jurisdictions
    const jurisdictionHierarchy = useMemo(() => ({
        "United States": {
            "Federal": [
                "Supreme Court", "Circuit Courts", "District Courts", 
                "Bankruptcy Courts", "Tax Courts", "Claims Courts",
                "Court of International Trade", "Foreign Intelligence Surveillance Court"
            ],
            "State": [
                "Alabama", "Alaska", "Arizona", "Arkansas", "California",
                "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
                "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
                "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
                "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
                "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
                "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
                "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
                "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
                "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
            ],
            "Federal Agencies": [
                "Department of Justice", "Department of Treasury", "Department of Defense",
                "Department of State", "Department of Commerce", "Department of Labor",
                "Environmental Protection Agency", "Securities and Exchange Commission"
            ]
        },
        "European Union": {
            "EU Institutions": [
                "Court of Justice of the European Union", "European Commission",
                "European Parliament", "Council of the European Union",
                "European Central Bank", "European Court of Auditors"
            ],
            "Member States": [
                "Germany", "France", "Italy", "Spain", "Netherlands",
                "Belgium", "Austria", "Sweden", "Denmark", "Finland",
                "Ireland", "Luxembourg", "Portugal", "Greece", "Poland",
                "Czech Republic", "Hungary", "Slovakia", "Slovenia", "Estonia",
                "Latvia", "Lithuania", "Malta", "Cyprus", "Croatia", "Bulgaria", "Romania"
            ]
        },
        "Commonwealth": {
            "United Kingdom": [
                "Supreme Court", "Court of Appeal", "High Court", "County Courts",
                "Crown Courts", "Magistrates' Courts", "Employment Tribunals"
            ],
            "Canada": [
                "Supreme Court of Canada", "Federal Court", "Federal Court of Appeal",
                "Alberta", "British Columbia", "Manitoba", "New Brunswick",
                "Newfoundland and Labrador", "Nova Scotia", "Ontario",
                "Prince Edward Island", "Quebec", "Saskatchewan",
                "Northwest Territories", "Nunavut", "Yukon"
            ],
            "Australia": [
                "High Court of Australia", "Federal Court", "Federal Circuit Court",
                "New South Wales", "Victoria", "Queensland", "Western Australia",
                "South Australia", "Tasmania", "Australian Capital Territory", "Northern Territory"
            ],
            "Other Commonwealth": [
                "New Zealand", "South Africa", "India", "Singapore", "Hong Kong"
            ]
        },
        "Asia Pacific": {
            "East Asia": ["Japan", "South Korea", "China", "Taiwan", "Hong Kong"],
            "Southeast Asia": ["Singapore", "Malaysia", "Thailand", "Indonesia", "Philippines", "Vietnam"],
            "South Asia": ["India", "Pakistan", "Bangladesh", "Sri Lanka"],
            "Oceania": ["Australia", "New Zealand", "Fiji", "Papua New Guinea"]
        },
        "Americas": {
            "North America": ["United States", "Canada", "Mexico"],
            "Central America": ["Guatemala", "Belize", "El Salvador", "Honduras", "Nicaragua", "Costa Rica", "Panama"],
            "South America": ["Brazil", "Argentina", "Chile", "Peru", "Colombia", "Venezuela", "Ecuador", "Bolivia", "Uruguay", "Paraguay"]
        },
        "Africa & Middle East": {
            "Africa": ["South Africa", "Nigeria", "Kenya", "Ghana", "Egypt", "Morocco"],
            "Middle East": ["Israel", "United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait"]
        },
        "International Organizations": {
            "Global": [
                "International Court of Justice", "International Criminal Court",
                "World Trade Organization", "United Nations", "World Bank",
                "International Monetary Fund", "European Court of Human Rights"
            ],
            "Regional": [
                "Inter-American Court of Human Rights", "African Court on Human and Peoples' Rights",
                "ASEAN", "Organization of American States", "African Union"
            ]
        }
    }), []);

    // Comprehensive document types
    const documentTypes = useMemo(() => [
        "Case Law", "Statutes", "Regulations", "Treaties", "Constitutions",
        "Scholarly Articles", "Legal News", "Bar Publications", "Law Reviews",
        "Administrative Decisions", "Court Orders", "Legal Briefs",
        "Government Reports", "Legislative Materials", "International Agreements",
        "Professional Guidelines", "Ethics Opinions", "Legal Commentaries"
    ], []);

    // Handle ultra-comprehensive search
    const handleUltraSearch = useCallback(async (searchQuery, additionalFilters = {}) => {
        setIsSearching(true);
        setSearchError(null);
        
        try {
            // Combine active filters with search-specific filters
            const combinedFilters = {
                ...activeFilters,
                ...additionalFilters,
                queryText: searchQuery
            };

            // Perform the search using our ultra-scale API
            const results = await performSearch(combinedFilters, currentPage, resultsPerPage);
            
            setSearchResults(results.documents || []);
            setTotalDocuments(results.totalCount || 0);
            
            // Update page if results change the total
            if (results.totalPages && currentPage > results.totalPages) {
                setCurrentPage(1);
            }

        } catch (error) {
            console.error('Ultra search failed:', error);
            setSearchError(error.message || 'Search failed. Please try again.');
            setSearchResults([]);
        } finally {
            setIsSearching(false);
        }
    }, [activeFilters, currentPage, resultsPerPage, performSearch]);

    // Load system status on mount and periodically
    useEffect(() => {
        const loadSystemStatus = async () => {
            try {
                const status = await ultraApiService.getSystemStatus();
                setSystemStatus({
                    operationalLevel: status.operational_level || 0,
                    activeSources: status.source_integration_status?.active_sources || 0,
                    totalSources: status.source_integration_status?.total_sources || 0,
                    lastUpdate: new Date()
                });
            } catch (error) {
                console.error('Failed to load system status:', error);
            }
        };

        // Initial load
        loadSystemStatus();

        // Refresh every 30 seconds
        const statusInterval = setInterval(loadSystemStatus, 30000);

        return () => clearInterval(statusInterval);
    }, []);

    // Handle filter changes
    const updateFilters = useCallback((filterType, value) => {
        setActiveFilters(prev => ({
            ...prev,
            [filterType]: value
        }));
        
        // Reset to first page when filters change
        setCurrentPage(1);
    }, []);

    // Handle pagination
    const handlePageChange = useCallback((newPage) => {
        setCurrentPage(newPage);
    }, []);

    // Real-time metrics display
    const systemMetrics = useMemo(() => ({
        documentsSearched: totalDocuments,
        sourcesActive: systemStatus.activeSources,
        sourcesTotal: systemStatus.totalSources,
        operationalLevel: systemStatus.operationalLevel,
        responseTime: searchMetrics?.averageResponseTime || 0,
        successRate: (systemStatus.activeSources / Math.max(systemStatus.totalSources, 1)) * 100
    }), [totalDocuments, systemStatus, searchMetrics]);

    return (
        <div className="ultra-legal-search-app min-h-screen bg-gray-50">
            {/* Ultra-Scale Header */}
            <header className="bg-gradient-to-r from-blue-900 via-purple-900 to-indigo-900 text-white shadow-2xl">
                <div className="container mx-auto px-6 py-8">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <div className="p-3 bg-white/20 rounded-lg backdrop-blur-sm">
                                <Search className="w-8 h-8" />
                            </div>
                            <div>
                                <h1 className="text-5xl font-bold tracking-tight">
                                    Ultra-Comprehensive Legal Research
                                </h1>
                                <p className="text-xl mt-2 text-blue-100">
                                    370M+ Legal Documents • 1,000+ Sources • 200+ Jurisdictions
                                </p>
                            </div>
                        </div>
                        
                        {/* Real-time system status indicators */}
                        <div className="flex items-center space-x-6">
                            <div className="text-center">
                                <div className="text-2xl font-bold text-green-300">
                                    {systemMetrics.operationalLevel.toFixed(1)}%
                                </div>
                                <div className="text-sm text-blue-200">System Health</div>
                            </div>
                            <div className="text-center">
                                <div className="text-2xl font-bold text-yellow-300">
                                    {systemMetrics.sourcesActive}/{systemMetrics.sourcesTotal}
                                </div>
                                <div className="text-sm text-blue-200">Active Sources</div>
                            </div>
                            <div className="text-center">
                                <div className="text-2xl font-bold text-cyan-300">
                                    {(totalDocuments / 1000000).toFixed(0)}M
                                </div>
                                <div className="text-sm text-blue-200">Documents</div>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Application Layout */}
            <div className="flex h-screen">
                {/* Advanced Filter Sidebar */}
                <div className={`${sidebarCollapsed ? 'w-16' : 'w-80'} bg-white shadow-xl border-r border-gray-200 transition-all duration-300 overflow-y-auto`}>
                    <div className="p-4">
                        {/* Sidebar Toggle */}
                        <button
                            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
                            className="w-full mb-4 p-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors flex items-center justify-center"
                        >
                            <Filter className="w-5 h-5" />
                            {!sidebarCollapsed && <span className="ml-2">Filters</span>}
                        </button>

                        {!sidebarCollapsed && (
                            <div className="space-y-6">
                                {/* Jurisdiction Browser */}
                                <div>
                                    <h3 className="text-lg font-semibold mb-3 text-gray-800 flex items-center">
                                        <Globe className="w-5 h-5 mr-2" />
                                        Jurisdictions
                                    </h3>
                                    <JurisdictionBrowser 
                                        hierarchy={jurisdictionHierarchy}
                                        selectedJurisdictions={activeFilters.jurisdictions}
                                        onSelectionChange={(selected) => updateFilters('jurisdictions', selected)}
                                    />
                                </div>

                                {/* Document Type Filter */}
                                <div>
                                    <h3 className="text-lg font-semibold mb-3 text-gray-800">
                                        Document Types
                                    </h3>
                                    <DocumentTypeFilter 
                                        types={documentTypes}
                                        selectedTypes={activeFilters.documentTypes}
                                        onSelectionChange={(selected) => updateFilters('documentTypes', selected)}
                                    />
                                </div>

                                {/* Source Health Monitor */}
                                <div>
                                    <h3 className="text-lg font-semibold mb-3 text-gray-800 flex items-center">
                                        <Activity className="w-5 h-5 mr-2" />
                                        Source Health
                                    </h3>
                                    <SourceHealthMonitor />
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Main Search Interface */}
                <div className="flex-1 flex flex-col overflow-hidden">
                    {/* Search Bar Section */}
                    <div className="bg-white shadow-sm border-b border-gray-200 p-6">
                        <UltraSearchBar 
                            onSearch={handleUltraSearch}
                            filters={activeFilters}
                            isSearching={isSearching}
                            searchSuggestions={searchSuggestions}
                            recentSearches={recentSearches}
                            onClearHistory={clearSearchHistory}
                        />
                        
                        {searchError && (
                            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                                <p className="text-red-700">{searchError}</p>
                            </div>
                        )}
                    </div>

                    {/* Search Results */}
                    <div className="flex-1 p-6 overflow-y-auto">
                        <SearchResults 
                            results={searchResults}
                            totalCount={totalDocuments}
                            isLoading={isSearching}
                            currentPage={currentPage}
                            resultsPerPage={resultsPerPage}
                            onPageChange={handlePageChange}
                            onResultsPerPageChange={setResultsPerPage}
                            searchMetrics={searchMetrics}
                        />
                    </div>
                </div>

                {/* Real-time Analytics Panel */}
                <div className={`${analyticsExpanded ? 'w-96' : 'w-16'} bg-gray-50 shadow-xl border-l border-gray-200 transition-all duration-300 overflow-y-auto`}>
                    <div className="p-4">
                        {/* Analytics Toggle */}
                        <button
                            onClick={() => setAnalyticsExpanded(!analyticsExpanded)}
                            className="w-full mb-4 p-2 bg-white hover:bg-gray-100 rounded-lg transition-colors flex items-center justify-center shadow-sm"
                        >
                            <BarChart3 className="w-5 h-5" />
                            {analyticsExpanded && <span className="ml-2">Analytics</span>}
                        </button>

                        {analyticsExpanded && (
                            <div className="space-y-6">
                                {/* Real-time Analytics */}
                                <div>
                                    <h3 className="text-lg font-semibold mb-3 text-gray-800 flex items-center">
                                        <TrendingUp className="w-5 h-5 mr-2" />
                                        Real-time Analytics
                                    </h3>
                                    <RealTimeAnalytics 
                                        metrics={systemMetrics}
                                        searchResults={searchResults}
                                    />
                                </div>

                                {/* Citation Network Visualization */}
                                <div>
                                    <h3 className="text-lg font-semibold mb-3 text-gray-800">
                                        Citation Network
                                    </h3>
                                    <CitationNetworkVisualization 
                                        documents={searchResults.slice(0, 10)} // Top 10 for visualization
                                    />
                                </div>

                                {/* Global Coverage Map */}
                                <div>
                                    <h3 className="text-lg font-semibold mb-3 text-gray-800">
                                        Global Coverage
                                    </h3>
                                    <GlobalCoverageMap 
                                        jurisdictions={activeFilters.jurisdictions}
                                        searchResults={searchResults}
                                    />
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UltraLegalSearchApp;