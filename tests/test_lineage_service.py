import pytest
from datetime import datetime
from data_mesh.lineage.lineage_service import (
    DataLineageService,
    DataNode,
    DataEdge
)

@pytest.fixture
def lineage_service():
    """Fixture to create a fresh lineage service instance for each test."""
    return DataLineageService()

@pytest.fixture
def sample_nodes():
    """Fixture to create sample nodes for testing."""
    return [
        DataNode(
            id="source1",
            name="Source Database 1",
            type="source",
            metadata={"database": "postgres", "schema": "public"}
        ),
        DataNode(
            id="transform1",
            name="ETL Process 1",
            type="transformation",
            metadata={"type": "spark_job", "version": "1.0"}
        ),
        DataNode(
            id="target1",
            name="Data Warehouse 1",
            type="target",
            metadata={"database": "snowflake", "schema": "analytics"}
        )
    ]

@pytest.fixture
def sample_edges(sample_nodes):
    """Fixture to create sample edges for testing."""
    return [
        DataEdge(
            source_id="source1",
            target_id="transform1",
            transformation_type="extract",
            metadata={"frequency": "daily"}
        ),
        DataEdge(
            source_id="transform1",
            target_id="target1",
            transformation_type="load",
            metadata={"frequency": "daily"}
        )
    ]

def test_add_node(lineage_service, sample_nodes):
    """Test adding nodes to the lineage graph."""
    for node in sample_nodes:
        lineage_service.add_node(node)
        assert node.id in lineage_service.nodes
        assert lineage_service.nodes[node.id] == node

def test_add_edge(lineage_service, sample_nodes, sample_edges):
    """Test adding edges to the lineage graph."""
    # Add nodes first
    for node in sample_nodes:
        lineage_service.add_node(node)
    
    # Add edges
    for edge in sample_edges:
        lineage_service.add_edge(edge)
        assert edge in lineage_service.edges

def test_add_edge_missing_node(lineage_service):
    """Test adding an edge with missing nodes."""
    edge = DataEdge(
        source_id="nonexistent",
        target_id="also_nonexistent",
        transformation_type="test",
        metadata={}
    )
    with pytest.raises(ValueError, match="Source or target node not found"):
        lineage_service.add_edge(edge)

def test_get_node(lineage_service, sample_nodes):
    """Test retrieving a node by ID."""
    for node in sample_nodes:
        lineage_service.add_node(node)
        retrieved_node = lineage_service.get_node(node.id)
        assert retrieved_node == node

def test_get_upstream_nodes(lineage_service, sample_nodes, sample_edges):
    """Test retrieving upstream nodes."""
    # Setup graph
    for node in sample_nodes:
        lineage_service.add_node(node)
    for edge in sample_edges:
        lineage_service.add_edge(edge)
    
    # Test upstream nodes for transform1
    upstream = lineage_service.get_upstream_nodes("transform1")
    assert len(upstream) == 1
    assert upstream[0].id == "source1"

def test_get_downstream_nodes(lineage_service, sample_nodes, sample_edges):
    """Test retrieving downstream nodes."""
    # Setup graph
    for node in sample_nodes:
        lineage_service.add_node(node)
    for edge in sample_edges:
        lineage_service.add_edge(edge)
    
    # Test downstream nodes for transform1
    downstream = lineage_service.get_downstream_nodes("transform1")
    assert len(downstream) == 1
    assert downstream[0].id == "target1"

def test_get_lineage_path(lineage_service, sample_nodes, sample_edges):
    """Test retrieving lineage path between nodes."""
    # Setup graph
    for node in sample_nodes:
        lineage_service.add_node(node)
    for edge in sample_edges:
        lineage_service.add_edge(edge)
    
    # Test path from source1 to target1
    path = lineage_service.get_lineage_path("source1", "target1")
    assert len(path) == 2
    assert path[0].source_id == "source1"
    assert path[0].target_id == "transform1"
    assert path[1].source_id == "transform1"
    assert path[1].target_id == "target1"

def test_get_impact_analysis(lineage_service, sample_nodes, sample_edges):
    """Test impact analysis for a node."""
    # Setup graph
    for node in sample_nodes:
        lineage_service.add_node(node)
    for edge in sample_edges:
        lineage_service.add_edge(edge)
    
    # Test impact analysis for transform1
    impact = lineage_service.get_impact_analysis("transform1")
    assert impact["node"].id == "transform1"
    assert impact["downstream_impact"]["direct"] == 1
    assert impact["upstream_dependencies"]["direct"] == 1

def test_get_graph_summary(lineage_service, sample_nodes, sample_edges):
    """Test retrieving graph summary."""
    # Setup graph
    for node in sample_nodes:
        lineage_service.add_node(node)
    for edge in sample_edges:
        lineage_service.add_edge(edge)
    
    summary = lineage_service.get_graph_summary()
    assert summary["total_nodes"] == 3
    assert summary["total_edges"] == 2
    assert summary["node_types"]["source"] == 1
    assert summary["node_types"]["transformation"] == 1
    assert summary["node_types"]["target"] == 1 