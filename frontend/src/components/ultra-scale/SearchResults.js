/**
 * Search Results - Advanced result display with rich analytics
 * Optimized for 370M+ document display with intelligent pagination
 */

import React, { useState, useMemo, useCallback } from 'react';
import { 
    FileText, Calendar, MapPin, Star, TrendingUp, 
    ExternalLink, Filter, Grid, List, ChevronLeft, 
    ChevronRight, Download, Share, Bookmark 
} from 'lucide-react';

const SearchResults = ({ 
    results = [], 
    totalCount = 0, 
    isLoading = false,
    currentPage = 1, 
    resultsPerPage = 50, 
    onPageChange,
    onResultsPerPageChange,
    searchMetrics = {}
}) => {
    const [viewMode, setViewMode] = useState('list'); // 'list' | 'grid'
    const [sortBy, setSortBy] = useState('relevance'); // 'relevance' | 'date' | 'citations' | 'confidence'
    const [showFilters, setShowFilters] = useState(false);

    // Calculate pagination info
    const totalPages = Math.ceil(totalCount / resultsPerPage);
    const startResult = (currentPage - 1) * resultsPerPage + 1;
    const endResult = Math.min(currentPage * resultsPerPage, totalCount);

    // Sort results
    const sortedResults = useMemo(() => {
        if (!results.length) return [];
        
        const sorted = [...results];
        
        switch (sortBy) {
            case 'date':
                return sorted.sort((a, b) => 
                    new Date(b.date_published || 0) - new Date(a.date_published || 0)
                );
            case 'citations':
                return sorted.sort((a, b) => (b.citation_count || 0) - (a.citation_count || 0));
            case 'confidence':
                return sorted.sort((a, b) => (b.confidence_score || 0) - (a.confidence_score || 0));
            default: // relevance
                return sorted.sort((a, b) => (b.relevance_score || 0) - (a.relevance_score || 0));
        }
    }, [results, sortBy]);

    // Format document type
    const formatDocumentType = (type) => {
        const typeMap = {
            'CASE_LAW': 'Case Law',
            'STATUTE': 'Statute',
            'REGULATION': 'Regulation',
            'TREATY': 'Treaty',
            'SCHOLARLY_ARTICLE': 'Scholarly Article',
            'LEGAL_NEWS': 'Legal News'
        };
        return typeMap[type] || type;
    };

    // Get document type icon
    const getDocumentIcon = (type) => {
        const iconMap = {
            'CASE_LAW': '⚖️',
            'STATUTE': '📜',
            'REGULATION': '📋',
            'TREATY': '🤝',
            'SCHOLARLY_ARTICLE': '📚',
            'LEGAL_NEWS': '📰'
        };
        return iconMap[type] || '📄';
    };

    // Format confidence score
    const getConfidenceLevel = (score) => {
        if (score >= 0.9) return { level: 'Very High', color: 'text-green-600 bg-green-100' };
        if (score >= 0.8) return { level: 'High', color: 'text-blue-600 bg-blue-100' };
        if (score >= 0.7) return { level: 'Medium', color: 'text-yellow-600 bg-yellow-100' };
        return { level: 'Low', color: 'text-red-600 bg-red-100' };
    };

    // Render pagination controls
    const renderPagination = () => {
        const maxPageButtons = 7;
        const halfRange = Math.floor(maxPageButtons / 2);
        
        let startPage = Math.max(1, currentPage - halfRange);
        let endPage = Math.min(totalPages, currentPage + halfRange);
        
        if (endPage - startPage + 1 < maxPageButtons) {
            if (startPage === 1) {
                endPage = Math.min(totalPages, startPage + maxPageButtons - 1);
            } else {
                startPage = Math.max(1, endPage - maxPageButtons + 1);
            }
        }
        
        const pageNumbers = [];
        for (let i = startPage; i <= endPage; i++) {
            pageNumbers.push(i);
        }

        return (
            <div className="flex items-center justify-between py-4">
                <div className="flex items-center space-x-4">
                    <div className="text-sm text-gray-600">
                        Showing {startResult.toLocaleString()}-{endResult.toLocaleString()} of {totalCount.toLocaleString()} results
                    </div>
                    
                    <select
                        value={resultsPerPage}
                        onChange={(e) => onResultsPerPageChange(parseInt(e.target.value))}
                        className="px-3 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value={25}>25 per page</option>
                        <option value={50}>50 per page</option>
                        <option value={100}>100 per page</option>
                    </select>
                </div>

                <div className="flex items-center space-x-2">
                    {/* Previous Button */}
                    <button
                        onClick={() => onPageChange(currentPage - 1)}
                        disabled={currentPage === 1}
                        className="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                    >
                        <ChevronLeft className="w-4 h-4 mr-1" />
                        Previous
                    </button>

                    {/* Page Numbers */}
                    {startPage > 1 && (
                        <>
                            <button
                                onClick={() => onPageChange(1)}
                                className="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50"
                            >
                                1
                            </button>
                            {startPage > 2 && <span className="text-gray-500">...</span>}
                        </>
                    )}

                    {pageNumbers.map(pageNum => (
                        <button
                            key={pageNum}
                            onClick={() => onPageChange(pageNum)}
                            className={`px-3 py-2 text-sm border rounded-lg ${
                                pageNum === currentPage
                                    ? 'bg-blue-600 text-white border-blue-600'
                                    : 'border-gray-300 hover:bg-gray-50'
                            }`}
                        >
                            {pageNum}
                        </button>
                    ))}

                    {endPage < totalPages && (
                        <>
                            {endPage < totalPages - 1 && <span className="text-gray-500">...</span>}
                            <button
                                onClick={() => onPageChange(totalPages)}
                                className="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50"
                            >
                                {totalPages}
                            </button>
                        </>
                    )}

                    {/* Next Button */}
                    <button
                        onClick={() => onPageChange(currentPage + 1)}
                        disabled={currentPage === totalPages}
                        className="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                    >
                        Next
                        <ChevronRight className="w-4 h-4 ml-1" />
                    </button>
                </div>
            </div>
        );
    };

    // Render individual result item
    const renderResultItem = (result, index) => {
        const confidence = getConfidenceLevel(result.confidence_score || 0);
        
        return (
            <div 
                key={result.id || index} 
                className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow duration-200"
            >
                {/* Header with document type and actions */}
                <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                        <span className="text-2xl">{getDocumentIcon(result.document_type)}</span>
                        <div>
                            <span className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full">
                                {formatDocumentType(result.document_type)}
                            </span>
                            <div className={`inline-block ml-2 px-2 py-1 text-xs rounded-full ${confidence.color}`}>
                                {confidence.level} Confidence
                            </div>
                        </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                        <button className="p-1 hover:bg-gray-100 rounded" title="Bookmark">
                            <Bookmark className="w-4 h-4 text-gray-500" />
                        </button>
                        <button className="p-1 hover:bg-gray-100 rounded" title="Share">
                            <Share className="w-4 h-4 text-gray-500" />
                        </button>
                        <button className="p-1 hover:bg-gray-100 rounded" title="Download">
                            <Download className="w-4 h-4 text-gray-500" />
                        </button>
                    </div>
                </div>

                {/* Title */}
                <h3 className="text-lg font-semibold text-gray-900 mb-2 hover:text-blue-600 cursor-pointer">
                    {result.title}
                </h3>

                {/* Snippet */}
                {result.snippet && (
                    <p className="text-gray-600 text-sm mb-3 line-clamp-3">
                        {result.snippet}
                    </p>
                )}

                {/* Metadata */}
                <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-3">
                    {result.jurisdiction && (
                        <div className="flex items-center">
                            <MapPin className="w-4 h-4 mr-1" />
                            {result.jurisdiction}
                        </div>
                    )}
                    
                    {result.court && (
                        <div className="flex items-center">
                            <FileText className="w-4 h-4 mr-1" />
                            {result.court}
                        </div>
                    )}
                    
                    {result.date_published && (
                        <div className="flex items-center">
                            <Calendar className="w-4 h-4 mr-1" />
                            {new Date(result.date_published).toLocaleDateString()}
                        </div>
                    )}
                    
                    {result.citation_count > 0 && (
                        <div className="flex items-center">
                            <TrendingUp className="w-4 h-4 mr-1" />
                            {result.citation_count} citations
                        </div>
                    )}
                </div>

                {/* Source and relevance score */}
                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                    <div className="flex items-center text-sm">
                        <span className="text-gray-500">Source:</span>
                        <span className="ml-1 font-medium text-gray-700">{result.source}</span>
                        {result.shard_source && (
                            <span className="ml-2 text-xs text-gray-400">({result.shard_source})</span>
                        )}
                    </div>
                    
                    <div className="flex items-center space-x-4">
                        <div className="flex items-center text-sm">
                            <Star className="w-4 h-4 text-yellow-500 mr-1" />
                            <span className="font-medium">
                                {(result.relevance_score || 0).toFixed(2)}
                            </span>
                        </div>
                        
                        <button className="flex items-center text-sm text-blue-600 hover:text-blue-800">
                            <ExternalLink className="w-4 h-4 mr-1" />
                            View Document
                        </button>
                    </div>
                </div>
            </div>
        );
    };

    if (isLoading) {
        return (
            <div className="search-results">
                {/* Loading State */}
                <div className="flex items-center justify-center py-12">
                    <div className="text-center">
                        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                        <p className="text-lg text-gray-600">Searching 370M+ legal documents...</p>
                        <p className="text-sm text-gray-400 mt-2">
                            {searchMetrics.averageResponseTime 
                                ? `Average search time: ${searchMetrics.averageResponseTime.toFixed(0)}ms`
                                : 'Please wait while we process your query'
                            }
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="search-results">
            {/* Results Header */}
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-4">
                    <h2 className="text-2xl font-bold text-gray-900">
                        Search Results
                    </h2>
                    <div className="text-sm text-gray-600">
                        {totalCount.toLocaleString()} documents found
                        {searchMetrics.executionTimeMs && (
                            <span className="ml-2">
                                in {searchMetrics.executionTimeMs}ms
                            </span>
                        )}
                    </div>
                </div>

                <div className="flex items-center space-x-4">
                    {/* Sort Options */}
                    <select
                        value={sortBy}
                        onChange={(e) => setSortBy(e.target.value)}
                        className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="relevance">Sort by Relevance</option>
                        <option value="date">Sort by Date</option>
                        <option value="citations">Sort by Citations</option>
                        <option value="confidence">Sort by Confidence</option>
                    </select>

                    {/* View Mode Toggle */}
                    <div className="flex border border-gray-300 rounded-lg overflow-hidden">
                        <button
                            onClick={() => setViewMode('list')}
                            className={`p-2 ${viewMode === 'list' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'}`}
                            title="List View"
                        >
                            <List className="w-4 h-4" />
                        </button>
                        <button
                            onClick={() => setViewMode('grid')}
                            className={`p-2 ${viewMode === 'grid' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'}`}
                            title="Grid View"
                        >
                            <Grid className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>

            {/* Search Results */}
            {sortedResults.length > 0 ? (
                <div className={`${viewMode === 'grid' ? 'grid grid-cols-1 lg:grid-cols-2 gap-6' : 'space-y-6'}`}>
                    {sortedResults.map((result, index) => renderResultItem(result, index))}
                </div>
            ) : (
                <div className="text-center py-12">
                    <div className="text-6xl mb-4">🔍</div>
                    <h3 className="text-xl font-semibold text-gray-800 mb-2">No results found</h3>
                    <p className="text-gray-600 mb-4">
                        Try adjusting your search terms or filters to find what you're looking for.
                    </p>
                    <button 
                        onClick={() => window.location.reload()}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        Clear Search
                    </button>
                </div>
            )}

            {/* Pagination */}
            {totalCount > resultsPerPage && renderPagination()}
        </div>
    );
};

export default SearchResults;