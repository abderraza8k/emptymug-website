import React, { useEffect, useRef, useState, useCallback } from 'react';

interface Point {
  x: number;
  y: number;
  vx: number;
  vy: number;
}

interface VoronoiBackgroundProps {
  pointCount?: number;
  className?: string;
  opacity?: number;
}

const VoronoiBackground: React.FC<VoronoiBackgroundProps> = ({
  pointCount = 12,
  className = '',
  opacity = 0.3
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number>();
  const [points, setPoints] = useState<Point[]>([]);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  // Initialize points
  useEffect(() => {
    const initPoints = () => {
      const newPoints: Point[] = [];
      for (let i = 0; i < pointCount; i++) {
        newPoints.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
        });
      }
      setPoints(newPoints);
      setDimensions({ width: window.innerWidth, height: window.innerHeight });
    };

    initPoints();
    
    const handleResize = () => {
      setDimensions({ width: window.innerWidth, height: window.innerHeight });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [pointCount]);

  // Mouse move handler with throttling
  const handleMouseMove = useCallback((e: MouseEvent) => {
    setMousePos({ x: e.clientX, y: e.clientY });
  }, []);

  useEffect(() => {
    let throttleTimer: number | null = null;
    
    const throttledMouseMove = (e: MouseEvent) => {
      if (throttleTimer === null) {
        throttleTimer = window.setTimeout(() => {
          handleMouseMove(e);
          throttleTimer = null;
        }, 16); // ~60fps
      }
    };

    window.addEventListener('mousemove', throttledMouseMove);
    return () => {
      window.removeEventListener('mousemove', throttledMouseMove);
      if (throttleTimer) {
        clearTimeout(throttleTimer);
      }
    };
  }, [handleMouseMove]);

  // Distance function for Voronoi calculation
  const distance = (x1: number, y1: number, x2: number, y2: number) => {
    return Math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
  };

  // Optimized Voronoi drawing using line segments
  const drawVoronoi = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas || points.length === 0) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const { width, height } = dimensions;
    canvas.width = width;
    canvas.height = height;

    // Clear canvas with subtle gradient background
    const gradient = ctx.createLinearGradient(0, 0, width, height);
    gradient.addColorStop(0, 'rgba(249, 250, 251, 0.1)');
    gradient.addColorStop(1, 'rgba(243, 244, 246, 0.05)');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
    
    // Draw Voronoi edges using a simplified approach
    ctx.strokeStyle = `rgba(107, 114, 128, ${opacity * 0.6})`; // Darker grey
    ctx.lineWidth = 1;
    
    // Create Delaunay triangulation approximation for Voronoi edges
    for (let i = 0; i < points.length; i++) {
      for (let j = i + 1; j < points.length; j++) {
        const p1 = points[i];
        const p2 = points[j];
        const dist = distance(p1.x, p1.y, p2.x, p2.y);
        
        // Only draw edges between nearby points
        if (dist < Math.min(width, height) * 0.3) {
          // Calculate perpendicular bisector (Voronoi edge)
          const midX = (p1.x + p2.x) / 2;
          const midY = (p1.y + p2.y) / 2;
          
          // Perpendicular direction
          const dx = p2.y - p1.y;
          const dy = p1.x - p2.x;
          const length = Math.sqrt(dx * dx + dy * dy);
          
          if (length > 0) {
            const unitX = dx / length;
            const unitY = dy / length;
            
            // Extend line in both directions
            const lineLength = Math.min(200, dist * 0.5);
            const x1 = midX - unitX * lineLength;
            const y1 = midY - unitY * lineLength;
            const x2 = midX + unitX * lineLength;
            const y2 = midY + unitY * lineLength;
            
            // Fade based on distance from mouse
            const mouseDist = distance(midX, midY, mousePos.x, mousePos.y);
            const fade = Math.max(0.3, 1 - mouseDist / 300);
            
            ctx.strokeStyle = `rgba(107, 114, 128, ${opacity * 0.8 * fade})`;
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
          }
        }
      }
    }

    // Draw connection lines between nearby points
    ctx.strokeStyle = `rgba(107, 114, 128, ${opacity * 0.4})`;
    ctx.lineWidth = 0.8;
    
    for (let i = 0; i < points.length; i++) {
      for (let j = i + 1; j < points.length; j++) {
        const p1 = points[i];
        const p2 = points[j];
        const dist = distance(p1.x, p1.y, p2.x, p2.y);
        
        if (dist < 180) {
          const mouseDist = Math.min(
            distance(p1.x, p1.y, mousePos.x, mousePos.y),
            distance(p2.x, p2.y, mousePos.x, mousePos.y)
          );
          const fade = Math.max(0.4, 1 - mouseDist / 200);
          
          ctx.strokeStyle = `rgba(107, 114, 128, ${opacity * 0.6 * fade})`;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
    }

    // Draw points with mouse interaction
    points.forEach((point, index) => {
      const mouseDist = distance(point.x, point.y, mousePos.x, mousePos.y);
      const scale = mouseDist < 100 ? 1 + (100 - mouseDist) / 100 : 1;
      const alpha = mouseDist < 150 ? opacity * (1.5 + (150 - mouseDist) / 150) : opacity * 0.8;
      
      ctx.fillStyle = `rgba(107, 114, 128, ${Math.min(alpha, 1)})`;
      ctx.beginPath();
      ctx.arc(point.x, point.y, 2 * scale, 0, Math.PI * 2);
      ctx.fill();
      
      // Add glow effect for nearby points
      if (mouseDist < 80) {
        ctx.fillStyle = `rgba(59, 130, 246, ${(80 - mouseDist) / 80 * opacity * 0.3})`;
        ctx.beginPath();
        ctx.arc(point.x, point.y, 8 * scale, 0, Math.PI * 2);
        ctx.fill();
      }
    });
  }, [points, dimensions, opacity, mousePos]);

  // Animation loop
  useEffect(() => {
    const animate = () => {
      setPoints(prevPoints => 
        prevPoints.map(point => {
          let newX = point.x + point.vx;
          let newY = point.y + point.vy;
          let newVx = point.vx;
          let newVy = point.vy;

          // Mouse attraction
          const mouseDistance = distance(point.x, point.y, mousePos.x, mousePos.y);
          if (mouseDistance < 150) {
            const attraction = 0.002 * (150 - mouseDistance) / 150;
            const angle = Math.atan2(mousePos.y - point.y, mousePos.x - point.x);
            newVx += Math.cos(angle) * attraction;
            newVy += Math.sin(angle) * attraction;
          }

          // Boundary bouncing
          if (newX <= 0 || newX >= dimensions.width) {
            newVx = -newVx;
            newX = Math.max(0, Math.min(dimensions.width, newX));
          }
          if (newY <= 0 || newY >= dimensions.height) {
            newVy = -newVy;
            newY = Math.max(0, Math.min(dimensions.height, newY));
          }

          // Velocity dampening
          newVx *= 0.99;
          newVy *= 0.99;

          // Speed limiting
          const speed = Math.sqrt(newVx ** 2 + newVy ** 2);
          if (speed > 2) {
            newVx = (newVx / speed) * 2;
            newVy = (newVy / speed) * 2;
          }

          return {
            x: newX,
            y: newY,
            vx: newVx,
            vy: newVy,
          };
        })
      );

      drawVoronoi();
      animationFrameRef.current = requestAnimationFrame(animate);
    };

    if (points.length > 0 && dimensions.width > 0) {
      animate();
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [points.length, dimensions, mousePos, drawVoronoi]);

  return (
    <canvas
      ref={canvasRef}
      className={`fixed inset-0 pointer-events-none ${className}`}
      style={{ 
        zIndex: 0,
        width: '100%',
        height: '100%'
      }}
    />
  );
};

export default VoronoiBackground;
