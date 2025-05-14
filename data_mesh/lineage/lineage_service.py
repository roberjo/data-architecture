from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)

class DataNode(BaseModel):
    """Represents a node in the data lineage graph."""
    id: str
    name: str
    type: str  # source, transformation, target
    metadata: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class DataEdge(BaseModel):
    """Represents an edge in the data lineage graph."""
    source_id: str
    target_id: str
    transformation_type: str
    metadata: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)

class LineageGraph:
    """Represents the complete data lineage graph."""
    nodes: Dict[str, DataNode]
    edges: List[DataEdge]

class DataLineageService:
    """Service for managing data lineage information."""
    
    def __init__(self):
        self.nodes: Dict[str, DataNode] = {}
        self.edges: List[DataEdge] = []
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the lineage service."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def add_node(self, node: DataNode) -> None:
        """Add a new node to the lineage graph."""
        self.nodes[node.id] = node
        logger.info(f"Added node: {node.id}")
    
    def add_edge(self, edge: DataEdge) -> None:
        """Add a new edge to the lineage graph."""
        if edge.source_id not in self.nodes or edge.target_id not in self.nodes:
            raise ValueError("Source or target node not found")
        
        self.edges.append(edge)
        logger.info(f"Added edge: {edge.source_id} -> {edge.target_id}")
    
    def get_node(self, node_id: str) -> Optional[DataNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_upstream_nodes(self, node_id: str) -> List[DataNode]:
        """Get all upstream nodes for a given node."""
        upstream_edges = [e for e in self.edges if e.target_id == node_id]
        return [self.nodes[e.source_id] for e in upstream_edges]
    
    def get_downstream_nodes(self, node_id: str) -> List[DataNode]:
        """Get all downstream nodes for a given node."""
        downstream_edges = [e for e in self.edges if e.source_id == node_id]
        return [self.nodes[e.target_id] for e in downstream_edges]
    
    def get_lineage_path(self, source_id: str, target_id: str) -> List[DataEdge]:
        """Get the lineage path between two nodes."""
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError("Source or target node not found")
        
        # Simple BFS implementation for finding path
        queue = [(source_id, [])]
        visited = {source_id}
        
        while queue:
            current_id, path = queue.pop(0)
            
            if current_id == target_id:
                return path
            
            for edge in self.edges:
                if edge.source_id == current_id and edge.target_id not in visited:
                    visited.add(edge.target_id)
                    queue.append((edge.target_id, path + [edge]))
        
        return []
    
    def get_impact_analysis(self, node_id: str) -> Dict[str, Any]:
        """Get impact analysis for a node."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        
        downstream_nodes = self.get_downstream_nodes(node_id)
        upstream_nodes = self.get_upstream_nodes(node_id)
        
        return {
            "node": self.nodes[node_id],
            "downstream_impact": {
                "direct": len(downstream_nodes),
                "nodes": downstream_nodes
            },
            "upstream_dependencies": {
                "direct": len(upstream_nodes),
                "nodes": upstream_nodes
            }
        }
    
    def get_graph_summary(self) -> Dict[str, Any]:
        """Get summary of the lineage graph."""
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": {
                node_type: len([n for n in self.nodes.values() if n.type == node_type])
                for node_type in set(n.type for n in self.nodes.values())
            }
        }

# FastAPI application
app = FastAPI(title="Data Lineage Service")
lineage_service = DataLineageService()

class NodeRequest(BaseModel):
    """Request model for adding/updating nodes."""
    id: str
    name: str
    type: str
    metadata: Dict[str, Any]

class EdgeRequest(BaseModel):
    """Request model for adding edges."""
    source_id: str
    target_id: str
    transformation_type: str
    metadata: Dict[str, Any]

@app.post("/nodes", response_model=DataNode)
async def add_node(node: NodeRequest):
    """Add a new node to the lineage graph."""
    try:
        data_node = DataNode(**node.dict())
        lineage_service.add_node(data_node)
        return data_node
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/edges", response_model=DataEdge)
async def add_edge(edge: EdgeRequest):
    """Add a new edge to the lineage graph."""
    try:
        data_edge = DataEdge(**edge.dict())
        lineage_service.add_edge(data_edge)
        return data_edge
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/nodes/{node_id}", response_model=DataNode)
async def get_node(node_id: str):
    """Get a node by ID."""
    node = lineage_service.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
    return node

@app.get("/nodes/{node_id}/upstream")
async def get_upstream_nodes(node_id: str):
    """Get upstream nodes for a given node."""
    try:
        nodes = lineage_service.get_upstream_nodes(node_id)
        return {"nodes": nodes}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/nodes/{node_id}/downstream")
async def get_downstream_nodes(node_id: str):
    """Get downstream nodes for a given node."""
    try:
        nodes = lineage_service.get_downstream_nodes(node_id)
        return {"nodes": nodes}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/lineage/{source_id}/{target_id}")
async def get_lineage_path(source_id: str, target_id: str):
    """Get lineage path between two nodes."""
    try:
        path = lineage_service.get_lineage_path(source_id, target_id)
        return {"path": path}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/impact/{node_id}")
async def get_impact_analysis(node_id: str):
    """Get impact analysis for a node."""
    try:
        return lineage_service.get_impact_analysis(node_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/summary")
async def get_graph_summary():
    """Get summary of the lineage graph."""
    return lineage_service.get_graph_summary()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()} 