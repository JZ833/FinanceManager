// src/ForceDirectedGraph.jsx
import React, { useRef } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import SpriteText from 'three-spritetext';
import * as THREE from 'three';

// Example graph data
const data = {
  nodes: [
    { id: 'NYSE', type: 'exchange' },
    { id: 'Technology', type: 'sector' },
    { id: 'Financials', type: 'sector' },
    { id: 'Healthcare', type: 'sector' },
    { id: 'Energy', type: 'sector' },
    { id: 'Industrials', type: 'sector' },
    { id: 'Communication Services', type: 'sector' },
    { id: 'Consumer Discretionary', type: 'sector' },
    { id: 'Materials', type: 'sector' },
    { id: 'Real Estate', type: 'sector' },
    { id: 'Utilities', type: 'sector' },
    { id: 'Consumer Staples', type: 'sector' },

    // Stock nodes with their associated sector
    { id: 'AAPL', type: 'stock', sector: 'Technology' },
    { id: 'MSFT', type: 'stock', sector: 'Technology' },
    { id: 'JPM', type: 'stock', sector: 'Financials' },
    { id: 'BAC', type: 'stock', sector: 'Financials' }
  ],
  links: [
    // Connect the overall exchange to each sector
    { source: 'NYSE', target: 'Technology' },
    { source: 'NYSE', target: 'Financials' },
    { source: 'NYSE', target: 'Healthcare' },
    { source: 'NYSE', target: 'Energy' },
    { source: 'NYSE', target: 'Industrials' },
    { source: 'NYSE', target: 'Communication Services' },
    { source: 'NYSE', target: 'Consumer Discretionary' },
    { source: 'NYSE', target: 'Materials' },
    { source: 'NYSE', target: 'Real Estate' },
    { source: 'NYSE', target: 'Utilities' },
    { source: 'NYSE', target: 'Consumer Staples' },
    // Connect each stock to its sector central node
    { source: 'Technology', target: 'AAPL' },
    { source: 'Technology', target: 'MSFT' },
    { source: 'Financials', target: 'JPM' },
    { source: 'Financials', target: 'BAC' }
  ]
};

const ForceDirectedGraph = () => {
  const fgRef = useRef();

  // Custom node rendering function
  const nodeThreeObject = (node) => {
    // Create a group to hold the sphere and text label
    const group = new THREE.Group();

    // Set default properties based on node type
    let sphereRadius = 5;
    let sphereColor = 'green';
    let textSize = 4;
    if (node.type === 'exchange') {
      sphereRadius = 10;
      sphereColor = 'gold';
      textSize = 6;
    } else if (node.type === 'sector') {
      sphereRadius = 7;
      sphereColor = 'orange';
      textSize = 5;
    }

    // Create the sphere mesh
    const sphereGeo = new THREE.SphereGeometry(sphereRadius, 16, 16);
    const sphereMat = new THREE.MeshStandardMaterial({ color: sphereColor });
    const sphere = new THREE.Mesh(sphereGeo, sphereMat);
    group.add(sphere);

    // Create the text sprite for the node's id (stock or label)
    const textSprite = new SpriteText(node.id);
    textSprite.color = 'white';
    textSprite.textHeight = textSize;
    // Position the text above the sphere (adjust as needed)
    textSprite.position.set(0, sphereRadius + 2, 0);
    group.add(textSprite);

    return group;
  };

  return (
    <ForceGraph3D
      ref={fgRef}
      graphData={data}
      nodeLabel={node => `${node.id} (${node.type})`}
      nodeThreeObject={nodeThreeObject}
      linkDirectionalArrowLength={3}
      linkDirectionalArrowRelPos={1}
    />
  );
};

export default ForceDirectedGraph;
