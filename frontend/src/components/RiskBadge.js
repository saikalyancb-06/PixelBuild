import React from 'react';
import { Chip } from '@mui/material';
import {
  CheckCircle as SafeIcon,
  Warning as WarningIcon,
  Dangerous as DangerIcon,
} from '@mui/icons-material';

const RiskBadge = ({ riskScore, size = 'medium' }) => {
  const getRiskLevel = (score) => {
    if (score === 0) return 'safe';
    if (score < 50) return 'low';
    if (score < 75) return 'medium';
    return 'high';
  };

  const getRiskConfig = (score) => {
    const level = getRiskLevel(score);
    
    const configs = {
      safe: {
        label: 'SAFE',
        color: '#4caf50',
        bgColor: '#e8f5e9',
        icon: <SafeIcon />
      },
      low: {
        label: 'LOW RISK',
        color: '#ff9800',
        bgColor: '#fff3e0',
        icon: <WarningIcon />
      },
      medium: {
        label: 'SUSPICIOUS',
        color: '#ff9800',
        bgColor: '#fff3e0',
        icon: <WarningIcon />
      },
      high: {
        label: 'DANGEROUS',
        color: '#f44336',
        bgColor: '#ffebee',
        icon: <DangerIcon />
      }
    };

    return configs[level];
  };

  const config = getRiskConfig(riskScore);

  return (
    <Chip
      icon={config.icon}
      label={`${config.label} (${riskScore}/100)`}
      size={size}
      sx={{
        backgroundColor: config.bgColor,
        color: config.color,
        fontWeight: 'bold',
        border: `2px solid ${config.color}`,
        '& .MuiChip-icon': {
          color: config.color
        }
      }}
    />
  );
};

export default RiskBadge;
