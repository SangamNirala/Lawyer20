/**
 * Document Type Filter - Advanced document classification filtering
 * Supports comprehensive document types with intelligent categorization
 */

import React, { useState, useMemo, useCallback } from 'react';
import { 
    FileText, Scale, Book, Newspaper, Building, 
    Gavel, Globe, Users, Check, Search 
} from 'lucide-react';

const DocumentTypeFilter = ({ types, selectedTypes = [], onSelectionChange }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [showAllTypes, setShowAllTypes] = useState(false);

    // Categorize document types with icons and descriptions
    const categorizedTypes = useMemo(() => {
        const categories = {
            'Primary Legal Sources': {
                icon: <Scale className="w-4 h-4" />,
                color: 'blue',
                types: ['Case Law', 'Statutes', 'Regulations', 'Constitutions', 'Treaties'],
                description: 'Binding legal authorities'
            },
            'Court Documents': {
                icon: <Gavel className="w-4 h-4" />,
                color: 'red',
                types: ['Court Orders', 'Administrative Decisions', 'Legal Briefs'],
                description: 'Court proceedings and decisions'
            },
            'Academic & Commentary': {
                icon: <Book className="w-4 h-4" />,
                color: 'green',
                types: ['Scholarly Articles', 'Law Reviews', 'Legal Commentaries'],
                description: 'Scholarly analysis and commentary'
            },
            'Professional Sources': {
                icon: <Users className="w-4 h-4" />,
                color: 'purple',
                types: ['Bar Publications', 'Professional Guidelines', 'Ethics Opinions'],
                description: 'Professional guidance and standards'
            },
            'News & Information': {
                icon: <Newspaper className="w-4 h-4" />,
                color: 'yellow',
                types: ['Legal News'],
                description: 'Legal news and current events'
            },
            'Government & Legislative': {
                icon: <Building className="w-4 h-4" />,
                color: 'indigo',
                types: ['Government Reports', 'Legislative Materials'],
                description: 'Government documents and legislative materials'
            },
            'International': {
                icon: <Globe className="w-4 h-4" />,
                color: 'cyan',
                types: ['International Agreements'],
                description: 'International legal documents'
            }
        };

        // Add any uncategorized types to "Other"
        const categorizedTypesList = Object.values(categories).flatMap(cat => cat.types);
        const otherTypes = types.filter(type => !categorizedTypesList.includes(type));
        
        if (otherTypes.length > 0) {
            categories['Other'] = {
                icon: <FileText className="w-4 h-4" />,
                color: 'gray',
                types: otherTypes,
                description: 'Other document types'
            };
        }

        return categories;
    }, [types]);

    // Filter types based on search
    const filteredTypes = useMemo(() => {
        if (!searchQuery) return types;
        
        return types.filter(type => 
            type.toLowerCase().includes(searchQuery.toLowerCase())
        );
    }, [types, searchQuery]);

    // Handle type selection
    const toggleType = useCallback((type) => {
        const newSelection = selectedTypes.includes(type)
            ? selectedTypes.filter(t => t !== type)
            : [...selectedTypes, type];
        
        onSelectionChange(newSelection);
    }, [selectedTypes, onSelectionChange]);

    // Select all types in a category
    const selectCategoryTypes = useCallback((categoryTypes, selectAll = true) => {
        if (selectAll) {
            const newSelection = [...new Set([...selectedTypes, ...categoryTypes])];
            onSelectionChange(newSelection);
        } else {
            const newSelection = selectedTypes.filter(t => !categoryTypes.includes(t));
            onSelectionChange(newSelection);
        }
    }, [selectedTypes, onSelectionChange]);

    // Check if all types in category are selected
    const isCategorySelected = useCallback((categoryTypes) => {
        return categoryTypes.every(type => selectedTypes.includes(type));
    }, [selectedTypes]);

    // Get color classes for category
    const getCategoryColorClasses = (color) => {
        const colors = {
            blue: 'bg-blue-50 border-blue-200 text-blue-700',
            red: 'bg-red-50 border-red-200 text-red-700',
            green: 'bg-green-50 border-green-200 text-green-700',
            purple: 'bg-purple-50 border-purple-200 text-purple-700',
            yellow: 'bg-yellow-50 border-yellow-200 text-yellow-700',
            indigo: 'bg-indigo-50 border-indigo-200 text-indigo-700',
            cyan: 'bg-cyan-50 border-cyan-200 text-cyan-700',
            gray: 'bg-gray-50 border-gray-200 text-gray-700'
        };
        return colors[color] || colors.gray;
    };

    // Get icon for document type
    const getTypeIcon = (type) => {
        const iconMap = {
            'Case Law': <Scale className="w-4 h-4" />,
            'Statutes': <Book className="w-4 h-4" />,
            'Regulations': <FileText className="w-4 h-4" />,
            'Court Orders': <Gavel className="w-4 h-4" />,
            'Legal News': <Newspaper className="w-4 h-4" />,
            'Government Reports': <Building className="w-4 h-4" />
        };
        return iconMap[type] || <FileText className="w-4 h-4" />;
    };

    const displayedCategories = showAllTypes 
        ? Object.entries(categorizedTypes)
        : Object.entries(categorizedTypes).slice(0, 4);

    return (
        <div className="document-type-filter">
            {/* Header */}
            <div className="flex items-center justify-between mb-3">
                <div className="text-sm text-gray-600">
                    {selectedTypes.length} of {types.length} selected
                </div>
                {selectedTypes.length > 0 && (
                    <button
                        onClick={() => onSelectionChange([])}
                        className="text-xs text-blue-600 hover:text-blue-800 transition-colors"
                    >
                        Clear All
                    </button>
                )}
            </div>

            {/* Search */}
            <div className="relative mb-4">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search document types..."
                    className="w-full pl-10 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

            {/* Search Results */}
            {searchQuery ? (
                <div className="space-y-2 max-h-64 overflow-y-auto">
                    {filteredTypes.length > 0 ? (
                        filteredTypes.map(type => (
                            <label
                                key={type}
                                className="flex items-center p-2 hover:bg-gray-50 rounded cursor-pointer"
                            >
                                <input
                                    type="checkbox"
                                    checked={selectedTypes.includes(type)}
                                    onChange={() => toggleType(type)}
                                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-3"
                                />
                                {getTypeIcon(type)}
                                <span className="ml-2 text-sm text-gray-700">{type}</span>
                            </label>
                        ))
                    ) : (
                        <div className="text-sm text-gray-500 text-center py-4">
                            No document types match your search
                        </div>
                    )}
                </div>
            ) : (
                /* Categorized View */
                <div className="space-y-3 max-h-80 overflow-y-auto">
                    {displayedCategories.map(([categoryName, category]) => {
                        const isAllSelected = isCategorySelected(category.types);
                        const someSelected = category.types.some(type => selectedTypes.includes(type));
                        
                        return (
                            <div 
                                key={categoryName} 
                                className={`border rounded-lg p-3 ${getCategoryColorClasses(category.color)}`}
                            >
                                {/* Category Header */}
                                <div className="flex items-center justify-between mb-2">
                                    <div className="flex items-center">
                                        {category.icon}
                                        <div className="ml-2">
                                            <div className="font-medium text-sm">{categoryName}</div>
                                            <div className="text-xs opacity-75">{category.description}</div>
                                        </div>
                                    </div>
                                    
                                    <button
                                        onClick={() => selectCategoryTypes(category.types, !isAllSelected)}
                                        className={`px-2 py-1 text-xs rounded transition-colors ${
                                            isAllSelected 
                                                ? 'bg-white/50 hover:bg-white/75' 
                                                : 'bg-white/30 hover:bg-white/50'
                                        }`}
                                    >
                                        {isAllSelected ? 'Deselect All' : 'Select All'}
                                    </button>
                                </div>

                                {/* Category Types */}
                                <div className="space-y-1">
                                    {category.types.map(type => (
                                        <label
                                            key={type}
                                            className="flex items-center p-1 hover:bg-white/30 rounded cursor-pointer transition-colors"
                                        >
                                            <input
                                                type="checkbox"
                                                checked={selectedTypes.includes(type)}
                                                onChange={() => toggleType(type)}
                                                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-2"
                                            />
                                            {getTypeIcon(type)}
                                            <span className="ml-2 text-sm">{type}</span>
                                        </label>
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                    
                    {/* Show More/Less Button */}
                    {Object.keys(categorizedTypes).length > 4 && (
                        <button
                            onClick={() => setShowAllTypes(!showAllTypes)}
                            className="w-full py-2 text-sm text-blue-600 hover:text-blue-800 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors"
                        >
                            {showAllTypes ? 'Show Less' : `Show ${Object.keys(categorizedTypes).length - 4} More Categories`}
                        </button>
                    )}
                </div>
            )}

            {/* Selected Types Summary */}
            {selectedTypes.length > 0 && (
                <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <div className="text-sm font-medium text-blue-800 mb-2">
                        Selected Types ({selectedTypes.length})
                    </div>
                    <div className="flex flex-wrap gap-1">
                        {selectedTypes.slice(0, 6).map(type => (
                            <span
                                key={type}
                                className="inline-flex items-center px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full"
                            >
                                {type}
                                <button
                                    onClick={() => toggleType(type)}
                                    className="ml-1 hover:text-blue-900"
                                >
                                    ×
                                </button>
                            </span>
                        ))}
                        {selectedTypes.length > 6 && (
                            <span className="text-xs text-blue-600">
                                +{selectedTypes.length - 6} more
                            </span>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default DocumentTypeFilter;