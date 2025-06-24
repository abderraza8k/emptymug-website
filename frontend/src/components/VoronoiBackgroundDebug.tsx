import React, { useEffect, useState } from 'react';

interface VoronoiBackgroundDebugProps {
  pointCount?: number;
  className?: string;
  opacity?: number;
}

const VoronoiBackgroundDebug: React.FC<VoronoiBackgroundDebugProps> = ({
  pointCount = 6,
  className = '',
  opacity = 0.3
}) => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null; // Avoid hydration issues
  }

  const floatKeyframes = `
    @keyframes float-debug {
      0%, 100% { 
        transform: translate(-50%, -50%) scale(1);
      }
      25% { 
        transform: translate(-50%, -50%) scale(1.05) translateX(20px);
      }
      50% { 
        transform: translate(-50%, -50%) scale(1.1) translateY(-25px);
      }
      75% { 
        transform: translate(-50%, -50%) scale(1.05) translateX(-20px);
      }
    }
  `;

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: floatKeyframes }} />
      <div 
        className={`fixed inset-0 pointer-events-none overflow-hidden ${className}`}
        style={{ 
          opacity,
          zIndex: 0,
        }}
      >
        {/* Debug version with high visibility */}
        <div 
          className="absolute top-10 left-10 rounded-full"
          style={{
            width: '300px',
            height: '300px',
            backgroundColor: '#3b82f6',
            opacity: 0.4,
            filter: 'blur(40px)',
            animation: 'float-debug 8s ease-in-out infinite',
          }}
        />
        <div 
          className="absolute top-20 right-20 rounded-full"
          style={{
            width: '250px',
            height: '250px',
            backgroundColor: '#9333ea',
            opacity:0.35,
            filter: 'blur(45px)',
            animation: 'float-debug 10s ease-in-out infinite 2s',
          }}
        />
        <div 
          className="absolute bottom-20 left-1/3 rounded-full"
          style={{
            width: '280px',
            height: '280px',
            backgroundColor: '#ec4899',
            opacity: 0.3,
            filter: 'blur(35px)',
            animation: 'float-debug 12s ease-in-out infinite 4s',
          }}
        />
        <div 
          className="absolute bottom-32 right-1/3 rounded-full"
          style={{
            width: '320px',
            height: '320px',
            backgroundColor: '#10b981',
            opacity: 0.25,
            filter: 'blur(50px)',
            animation: 'float-debug 9s ease-in-out infinite 6s',
          }}
        />
        <div 
          className="absolute top-1/2 left-1/2 rounded-full"
          style={{
            width: '400px',
            height: '400px',
            backgroundColor: '#f59e0b',
            opacity: 0.2,
            filter: 'blur(60px)',
            transform: 'translate(-50%, -50%)',
            animation: 'float-debug 15s ease-in-out infinite 8s',
          }}
        />
      </div>
    </>
  );
};

export default VoronoiBackgroundDebug;
