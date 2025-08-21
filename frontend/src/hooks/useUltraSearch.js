/**
 * Ultra-Scale Search Hook - Advanced search functionality
 * Custom hook for managing ultra-comprehensive search operations
 */

import { useState, useCallback, useEffect, useRef } from 'react';
import { ultraApiService } from '../services/ultraApiService';

export const useUltraSearch = () => {
    // Search state
    const [isSearching, setIsSearching] = useState(false);
    const [searchResults, setSearchResults] = useState([]);
    const [searchMetrics, setSearchMetrics] = useState({
        totalSearches: 0,
        successfulSearches: 0,
        averageResponseTime: 0,
        lastSearchTime: null,
        searchHistory: []
    });
    
    // Search suggestions and history
    const [searchSuggestions, setSearchSuggestions] = useState([]);
    const [recentSearches, setRecentSearches] = useState([]);
    const [suggestionCache, setSuggestionCache] = useState(new Map());
    
    // Performance tracking
    const searchTimeoutRef = useRef(null);
    const suggestionTimeoutRef = useRef(null);
    
    // Load search history from localStorage on mount
    useEffect(() => {
        try {
            const savedSearches = localStorage.getItem('ultra_search_history');
            if (savedSearches) {
                const parsed = JSON.parse(savedSearches);
                setRecentSearches(parsed.slice(0, 10)); // Keep last 10 searches
            }
            
            const savedMetrics = localStorage.getItem('ultra_search_metrics');
            if (savedMetrics) {
                const parsed = JSON.parse(savedMetrics);
                setSearchMetrics(prev => ({ ...prev, ...parsed }));
            }
        } catch (error) {
            console.error('Failed to load search history:', error);
        }
    }, []);

    // Save search history and metrics to localStorage
    const saveSearchData = useCallback((searches, metrics) => {
        try {
            localStorage.setItem('ultra_search_history', JSON.stringify(searches));
            localStorage.setItem('ultra_search_metrics', JSON.stringify(metrics));
        } catch (error) {
            console.error('Failed to save search data:', error);
        }
    }, []);

    // Add search to history
    const addToSearchHistory = useCallback((searchQuery, filters, results) => {
        const searchEntry = {
            id: Date.now(),
            query: searchQuery,
            filters: filters,
            timestamp: new Date().toISOString(),
            resultCount: results.totalCount || 0,
            executionTime: results.executionTimeMs || 0
        };

        setRecentSearches(prev => {
            const updated = [searchEntry, ...prev.filter(s => s.query !== searchQuery)].slice(0, 10);
            saveSearchData(updated, searchMetrics);
            return updated;
        });
    }, [searchMetrics, saveSearchData]);

    // Update search metrics
    const updateSearchMetrics = useCallback((executionTime, success = true) => {
        setSearchMetrics(prev => {
            const newMetrics = {
                ...prev,
                totalSearches: prev.totalSearches + 1,
                successfulSearches: success ? prev.successfulSearches + 1 : prev.successfulSearches,
                lastSearchTime: executionTime,
                searchHistory: [...(prev.searchHistory || []), {
                    timestamp: Date.now(),
                    executionTime,
                    success
                }].slice(-50) // Keep last 50 search records
            };

            // Calculate average response time
            const successfulTimes = newMetrics.searchHistory
                .filter(h => h.success && h.executionTime > 0)
                .map(h => h.executionTime);
            
            if (successfulTimes.length > 0) {
                newMetrics.averageResponseTime = 
                    successfulTimes.reduce((sum, time) => sum + time, 0) / successfulTimes.length;
            }

            return newMetrics;
        });
    }, []);

    // Get search suggestions with caching and debouncing
    const getSuggestions = useCallback(async (query) => {
        if (!query || query.length < 2) {
            setSearchSuggestions([]);
            return;
        }

        // Check cache first
        if (suggestionCache.has(query)) {
            setSearchSuggestions(suggestionCache.get(query));
            return;
        }

        // Clear previous timeout
        if (suggestionTimeoutRef.current) {
            clearTimeout(suggestionTimeoutRef.current);
        }

        // Debounce suggestion requests
        suggestionTimeoutRef.current = setTimeout(async () => {
            try {
                const response = await ultraApiService.getSearchSuggestions(query, 8);
                
                // Add recent searches that match
                const matchingRecent = recentSearches
                    .filter(search => 
                        search.query.toLowerCase().includes(query.toLowerCase()) &&
                        !response.suggestions.includes(search.query)
                    )
                    .map(search => search.query)
                    .slice(0, 3);

                const allSuggestions = [
                    ...response.suggestions,
                    ...matchingRecent
                ].slice(0, 8);

                setSearchSuggestions(allSuggestions);
                
                // Cache suggestions
                setSuggestionCache(prev => {
                    const newCache = new Map(prev);
                    newCache.set(query, allSuggestions);
                    
                    // Limit cache size
                    if (newCache.size > 100) {
                        const firstKey = newCache.keys().next().value;
                        newCache.delete(firstKey);
                    }
                    
                    return newCache;
                });

            } catch (error) {
                console.error('Failed to get search suggestions:', error);
                setSearchSuggestions([]);
            }
        }, 300); // 300ms debounce
    }, [recentSearches, suggestionCache]);

    // Perform ultra-comprehensive search
    const performSearch = useCallback(async (searchFilters, page = 1, perPage = 50) => {
        if (searchTimeoutRef.current) {
            clearTimeout(searchTimeoutRef.current);
        }

        setIsSearching(true);
        const startTime = performance.now();

        try {
            // Prepare search filter for API
            const ultraSearchFilter = {
                query_text: searchFilters.queryText,
                document_types: searchFilters.documentTypes,
                geographic: searchFilters.jurisdictions?.length > 0 ? {
                    jurisdictions: searchFilters.jurisdictions
                } : undefined,
                content: {
                    legal_topics: searchFilters.legalTopics,
                },
                quality: {
                    min_confidence_score: searchFilters.qualityFilter?.minConfidence || 0.7,
                    min_citation_count: searchFilters.qualityFilter?.minCitations || 0
                },
                courts: searchFilters.courts,
                sources: searchFilters.sources,
                date_ranges: searchFilters.dateRange ? [{
                    start_date: searchFilters.dateRange.start,
                    end_date: searchFilters.dateRange.end,
                    date_type: "published"
                }] : undefined
            };

            // Remove undefined fields
            Object.keys(ultraSearchFilter).forEach(key => {
                if (ultraSearchFilter[key] === undefined || 
                    (Array.isArray(ultraSearchFilter[key]) && ultraSearchFilter[key].length === 0)) {
                    delete ultraSearchFilter[key];
                }
            });

            const results = await ultraApiService.ultraSearch(ultraSearchFilter, page, perPage);
            const executionTime = performance.now() - startTime;

            // Update metrics
            updateSearchMetrics(executionTime, true);

            // Add to search history if it's a new search (page 1)
            if (page === 1 && searchFilters.queryText) {
                addToSearchHistory(searchFilters.queryText, searchFilters, results);
            }

            setSearchResults(results);
            
            return results;

        } catch (error) {
            console.error('Ultra search failed:', error);
            const executionTime = performance.now() - startTime;
            updateSearchMetrics(executionTime, false);
            
            throw new Error(`Search failed: ${error.message}`);
        } finally {
            setIsSearching(false);
        }
    }, [updateSearchMetrics, addToSearchHistory]);

    // Clear search history
    const clearSearchHistory = useCallback(() => {
        setRecentSearches([]);
        setSearchMetrics(prev => ({
            ...prev,
            searchHistory: []
        }));
        
        try {
            localStorage.removeItem('ultra_search_history');
            localStorage.removeItem('ultra_search_metrics');
        } catch (error) {
            console.error('Failed to clear search history:', error);
        }
    }, []);

    // Get search analytics
    const getSearchAnalytics = useCallback(() => {
        const analytics = ultraApiService.getPerformanceMetrics();
        
        return {
            ...analytics,
            localMetrics: searchMetrics,
            recentSearchesCount: recentSearches.length,
            cacheSize: suggestionCache.size
        };
    }, [searchMetrics, recentSearches.length, suggestionCache.size]);

    // Enhanced search with auto-suggestions
    const searchWithSuggestions = useCallback(async (query, filters = {}) => {
        // Get suggestions for empty or short queries
        if (!query || query.length < 3) {
            await getSuggestions(query);
        }

        // Only perform search if query is substantial
        if (query && query.length >= 2) {
            return await performSearch({ ...filters, queryText: query });
        }

        return null;
    }, [getSuggestions, performSearch]);

    // Auto-complete functionality
    const handleQueryInput = useCallback(async (query) => {
        await getSuggestions(query);
    }, [getSuggestions]);

    // Cleanup timeouts on unmount
    useEffect(() => {
        return () => {
            if (searchTimeoutRef.current) {
                clearTimeout(searchTimeoutRef.current);
            }
            if (suggestionTimeoutRef.current) {
                clearTimeout(suggestionTimeoutRef.current);
            }
        };
    }, []);

    return {
        // Core search functionality
        performSearch,
        searchWithSuggestions,
        isSearching,
        searchResults,

        // Search suggestions and history
        searchSuggestions,
        recentSearches,
        getSuggestions,
        handleQueryInput,
        clearSearchHistory,

        // Metrics and analytics
        searchMetrics,
        getSearchAnalytics,

        // Advanced features
        addToSearchHistory,
        updateSearchMetrics
    };
};