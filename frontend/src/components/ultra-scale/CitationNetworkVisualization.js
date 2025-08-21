/**
 * Citation Network Visualization - Interactive citation relationships
 * Displays citation networks and document relationships
 */

import React, { useState, useEffect, useRef, useMemo } from 'react';
import { 
    Network, Share2, TrendingUp, Eye, 
    ZoomIn, ZoomOut, RefreshCw, Download 
} from 'lucide-react';

const CitationNetworkVisualization = ({ documents = [] }) => {
    const [selectedNode, setSelectedNode] = useState(null);
    const [networkData, setNetworkData] = useState({ nodes: [], edges: [] });
    const [viewMode, setViewMode] = useState('network'); // 'network', 'hierarchy', 'timeline'
    const [isLoading, setIsLoading] = useState(false);
    const canvasRef = useRef(null);

    // Process documents to create network data
    useEffect(() => {
        if (documents.length === 0) return;

        setIsLoading(true);
        
        // Create nodes from documents
        const nodes = documents.map((doc, index) => ({
            id: doc.id || `doc_${index}`,
            label: doc.title?.substring(0, 50) + '...' || `Document ${index + 1}`,
            title: doc.title || `Document ${index + 1}`,
            type: doc.document_type || 'unknown',
            citations: doc.citation_count || 0,
            confidence: doc.confidence_score || 0,
            jurisdiction: doc.jurisdiction || 'Unknown',
            year: doc.date_published ? new Date(doc.date_published).getFullYear() : null,
            x: Math.random() * 300,
            y: Math.random() * 200,
            size: Math.max(5, Math.min(20, (doc.citation_count || 0) / 2 + 8))
        }));

        // Create synthetic citation relationships
        const edges = [];
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const nodeA = nodes[i];
                const nodeB = nodes[j];
                
                // Create edge based on similarity heuristics
                const shouldConnect = (
                    nodeA.type === nodeB.type ||
                    nodeA.jurisdiction === nodeB.jurisdiction ||
                    (nodeA.year && nodeB.year && Math.abs(nodeA.year - nodeB.year) <= 5)
                ) && Math.random() > 0.7; // 30% chance of connection

                if (shouldConnect) {
                    edges.push({
                        from: nodeA.id,
                        to: nodeB.id,
                        strength: Math.random() * 0.5 + 0.3,
                        type: nodeA.jurisdiction === nodeB.jurisdiction ? 'jurisdictional' : 'topical'
                    });
                }
            }
        }

        setNetworkData({ nodes, edges });
        setIsLoading(false);
    }, [documents]);

    // Get node color based on document type
    const getNodeColor = (type, confidence) => {
        const baseColors = {
            'CASE_LAW': '#3B82F6',
            'STATUTE': '#10B981', 
            'REGULATION': '#F59E0B',
            'TREATY': '#8B5CF6',
            'SCHOLARLY_ARTICLE': '#06B6D4',
            'LEGAL_NEWS': '#EF4444',
            'unknown': '#6B7280'
        };
        
        const alpha = Math.max(0.6, confidence);
        const color = baseColors[type] || baseColors.unknown;
        return `${color}${Math.round(alpha * 255).toString(16).padStart(2, '0')}`;
    };

    // Network statistics
    const networkStats = useMemo(() => {
        if (!networkData.nodes.length) return null;

        const totalCitations = networkData.nodes.reduce((sum, node) => sum + node.citations, 0);
        const avgCitations = totalCitations / networkData.nodes.length;
        const mostCited = networkData.nodes.reduce((max, node) => 
            node.citations > max.citations ? node : max, networkData.nodes[0]);
        
        const typeDistribution = networkData.nodes.reduce((dist, node) => {
            dist[node.type] = (dist[node.type] || 0) + 1;
            return dist;
        }, {});

        return {
            totalNodes: networkData.nodes.length,
            totalEdges: networkData.edges.length,
            avgCitations: avgCitations.toFixed(1),
            mostCited,
            typeDistribution,
            networkDensity: ((networkData.edges.length * 2) / (networkData.nodes.length * (networkData.nodes.length - 1))).toFixed(3)
        };
    }, [networkData]);

    // Simple network visualization (canvas-based)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas || !networkData.nodes.length) return;

        const ctx = canvas.getContext('2d');
        const rect = canvas.getBoundingClientRect();
        
        // Set canvas size
        canvas.width = rect.width;
        canvas.height = rect.height;

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw edges first
        networkData.edges.forEach(edge => {
            const fromNode = networkData.nodes.find(n => n.id === edge.from);
            const toNode = networkData.nodes.find(n => n.id === edge.to);
            
            if (fromNode && toNode) {
                ctx.beginPath();
                ctx.moveTo(fromNode.x, fromNode.y);
                ctx.lineTo(toNode.x, toNode.y);
                ctx.strokeStyle = edge.type === 'jurisdictional' ? '#3B82F6' : '#94A3B8';
                ctx.lineWidth = edge.strength * 2;
                ctx.stroke();
            }
        });

        // Draw nodes
        networkData.nodes.forEach(node => {
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.size, 0, 2 * Math.PI);
            ctx.fillStyle = getNodeColor(node.type, node.confidence);
            ctx.fill();
            
            // Highlight selected node
            if (selectedNode && selectedNode.id === node.id) {
                ctx.strokeStyle = '#1F2937';
                ctx.lineWidth = 3;
                ctx.stroke();
            }
            
            // Draw labels for important nodes
            if (node.citations > 5) {
                ctx.fillStyle = '#374151';
                ctx.font = '10px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(node.citations.toString(), node.x, node.y + node.size + 12);
            }
        });
    }, [networkData, selectedNode]);

    // Handle canvas click
    const handleCanvasClick = (event) => {
        const canvas = canvasRef.current;
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        // Find clicked node
        const clickedNode = networkData.nodes.find(node => {
            const distance = Math.sqrt((x - node.x) ** 2 + (y - node.y) ** 2);
            return distance <= node.size;
        });

        setSelectedNode(clickedNode || null);
    };

    if (isLoading) {
        return (
            <div className="citation-network p-4 bg-white rounded-lg border">
                <div className="flex items-center justify-center py-8">
                    <div className="text-center">
                        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
                        <p className="text-sm text-gray-600">Building citation network...</p>
                    </div>
                </div>
            </div>
        );
    }

    if (documents.length === 0) {
        return (
            <div className="citation-network p-4 bg-white rounded-lg border">
                <div className="text-center py-8">
                    <Network className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                    <p className="text-sm text-gray-500">No documents to visualize</p>
                    <p className="text-xs text-gray-400 mt-1">Perform a search to see citation relationships</p>
                </div>
            </div>
        );
    }

    return (
        <div className="citation-network">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                    <Network className="w-4 h-4 text-gray-600" />
                    <span className="text-sm font-medium">Citation Network</span>
                </div>
                
                <div className="flex items-center space-x-1">
                    <button
                        onClick={() => setViewMode(viewMode === 'network' ? 'hierarchy' : 'network')}
                        className="p-1 hover:bg-gray-100 rounded"
                        title="Toggle view mode"
                    >
                        <RefreshCw className="w-3 h-3 text-gray-500" />
                    </button>
                </div>
            </div>

            {/* Network Visualization */}
            <div className="relative">
                <canvas
                    ref={canvasRef}
                    onClick={handleCanvasClick}
                    className="w-full h-48 bg-gray-50 rounded border cursor-pointer"
                    style={{ minHeight: '192px' }}
                />
                
                {/* Legend */}
                <div className="absolute top-2 left-2 bg-white/90 backdrop-blur-sm rounded p-2 text-xs">
                    <div className="space-y-1">
                        <div className="flex items-center">
                            <div className="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
                            <span>Case Law</span>
                        </div>
                        <div className="flex items-center">
                            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                            <span>Statute</span>
                        </div>
                        <div className="flex items-center">
                            <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                            <span>Regulation</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Network Statistics */}
            {networkStats && (
                <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                    <div className="bg-blue-50 p-2 rounded">
                        <div className="font-medium text-blue-800">Nodes</div>
                        <div className="text-blue-600">{networkStats.totalNodes}</div>
                    </div>
                    <div className="bg-green-50 p-2 rounded">
                        <div className="font-medium text-green-800">Connections</div>
                        <div className="text-green-600">{networkStats.totalEdges}</div>
                    </div>
                    <div className="bg-purple-50 p-2 rounded">
                        <div className="font-medium text-purple-800">Avg Citations</div>
                        <div className="text-purple-600">{networkStats.avgCitations}</div>
                    </div>
                    <div className="bg-orange-50 p-2 rounded">
                        <div className="font-medium text-orange-800">Density</div>
                        <div className="text-orange-600">{networkStats.networkDensity}</div>
                    </div>
                </div>
            )}

            {/* Selected Node Info */}
            {selectedNode && (
                <div className="mt-4 p-3 bg-gray-50 border rounded-lg">
                    <div className="text-sm font-medium text-gray-800 mb-2">
                        {selectedNode.title}
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                        <div>Type: {selectedNode.type}</div>
                        <div>Citations: {selectedNode.citations}</div>
                        <div>Jurisdiction: {selectedNode.jurisdiction}</div>
                        <div>Confidence: {(selectedNode.confidence * 100).toFixed(1)}%</div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CitationNetworkVisualization;