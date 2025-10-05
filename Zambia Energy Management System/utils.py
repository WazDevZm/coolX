#!/usr/bin/env python3
"""
Utility functions for Zambia Energy Management System
===================================================

This module contains utility functions for data processing, 
calculations, and system utilities specific to Zambia's energy sector.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Tuple, Optional
import math

def calculate_grid_utilization(current_load: float, total_capacity: float) -> float:
    """Calculate grid utilization percentage"""
    return (current_load / total_capacity) * 100

def calculate_reserve_margin(current_load: float, total_capacity: float) -> float:
    """Calculate reserve margin percentage"""
    return ((total_capacity - current_load) / total_capacity) * 100

def predict_load_shedding_risk(utilization: float, reserve_margin: float) -> str:
    """Predict load shedding risk based on grid parameters"""
    if utilization > 95 or reserve_margin < 5:
        return "CRITICAL"
    elif utilization > 85 or reserve_margin < 15:
        return "HIGH"
    elif utilization > 75 or reserve_margin < 25:
        return "MEDIUM"
    else:
        return "LOW"

def calculate_seasonal_factor(month: int, is_dry_season: bool = True) -> float:
    """Calculate seasonal generation factor for Zambian climate"""
    if is_dry_season:
        # Dry season (April-October) - lower hydro, higher solar
        if month in [4, 5, 6, 7, 8, 9, 10]:
            return 0.7  # Reduced hydro generation
        else:
            return 1.0  # Normal hydro generation
    else:
        # Wet season (November-March) - higher hydro, lower solar
        return 1.0

def calculate_daily_load_pattern(hour: int) -> float:
    """Calculate daily load pattern factor for Zambian consumption"""
    # Peak hours: 6-9 AM and 6-9 PM
    if 6 <= hour <= 9:
        return 1.3  # Morning peak
    elif 18 <= hour <= 21:
        return 1.4  # Evening peak
    elif 22 <= hour <= 5:
        return 0.6  # Night time low
    else:
        return 1.0  # Normal load

def calculate_renewable_potential(month: int, hour: int) -> Dict[str, float]:
    """Calculate renewable energy potential for Zambia"""
    # Solar potential (higher in dry season)
    solar_factor = 1.0 if month in [4, 5, 6, 7, 8, 9, 10] else 0.8
    
    # Wind potential (higher in certain months)
    wind_factor = 1.0 if month in [5, 6, 7, 8] else 0.7
    
    # Hydro potential (higher in wet season)
    hydro_factor = 1.0 if month in [11, 12, 1, 2, 3] else 0.7
    
    return {
        'solar': solar_factor * (1.0 if 6 <= hour <= 18 else 0.0),
        'wind': wind_factor,
        'hydro': hydro_factor
    }

def optimize_load_shedding_schedule(zones: Dict, current_load: float, 
                                  total_capacity: float) -> List[Dict]:
    """Optimize load shedding schedule based on priority and demand"""
    utilization = calculate_grid_utilization(current_load, total_capacity)
    
    if utilization < 85:
        return []  # No load shedding needed
    
    # Sort zones by priority and population
    sorted_zones = sorted(zones.items(), 
                         key=lambda x: (x[1]['priority'] == 'high', x[1]['population']), 
                         reverse=True)
    
    shedding_schedule = []
    load_to_shed = current_load - (total_capacity * 0.8)  # Target 80% utilization
    
    for zone_name, zone_data in sorted_zones:
        if load_to_shed <= 0:
            break
            
        zone_demand = zone_data['average_demand_mw']
        if zone_demand <= load_to_shed:
            shedding_schedule.append({
                'zone': zone_name,
                'duration_hours': 2,
                'demand_reduction_mw': zone_demand,
                'priority': zone_data['priority']
            })
            load_to_shed -= zone_demand
    
    return shedding_schedule

def calculate_energy_efficiency_score(consumption_data: List[Dict]) -> float:
    """Calculate energy efficiency score based on consumption patterns"""
    if not consumption_data:
        return 0.0
    
    # Calculate average consumption
    avg_consumption = np.mean([d['load'] for d in consumption_data])
    
    # Calculate peak-to-average ratio
    peak_consumption = max([d['load'] for d in consumption_data])
    peak_ratio = peak_consumption / avg_consumption
    
    # Calculate efficiency score (lower peak ratio = higher efficiency)
    efficiency_score = max(0, 100 - (peak_ratio - 1) * 50)
    
    return min(100, efficiency_score)

def calculate_renewable_energy_share(generation_data: Dict) -> float:
    """Calculate renewable energy share in total generation"""
    total_generation = sum(generation_data.values())
    renewable_generation = generation_data.get('solar', 0) + generation_data.get('wind', 0)
    
    if total_generation == 0:
        return 0.0
    
    return (renewable_generation / total_generation) * 100

def predict_demand_forecast(historical_data: List[Dict], forecast_hours: int = 24) -> List[float]:
    """Predict future demand based on historical patterns"""
    if len(historical_data) < 24:
        return [0] * forecast_hours
    
    # Extract consumption values
    consumption = [d['load'] for d in historical_data]
    
    # Simple moving average with trend
    window_size = min(24, len(consumption))
    recent_avg = np.mean(consumption[-window_size:])
    
    # Calculate trend
    if len(consumption) >= 48:
        trend = np.polyfit(range(24), consumption[-24:], 1)[0]
    else:
        trend = 0
    
    # Generate forecast
    forecast = []
    for hour in range(forecast_hours):
        # Add trend and daily pattern
        daily_factor = calculate_daily_load_pattern((datetime.now().hour + hour) % 24)
        predicted_load = recent_avg + (trend * hour) * daily_factor
        forecast.append(max(0, predicted_load))
    
    return forecast

def calculate_carbon_footprint(generation_mix: Dict, total_generation: float) -> float:
    """Calculate carbon footprint in tonnes CO2"""
    # Emission factors (kg CO2 per kWh)
    emission_factors = {
        'coal': 0.820,
        'gas': 0.490,
        'oil': 0.650,
        'hydro': 0.024,
        'solar': 0.041,
        'wind': 0.011,
        'nuclear': 0.012
    }
    
    total_emissions = 0
    for source, amount in generation_mix.items():
        if source in emission_factors:
            total_emissions += amount * emission_factors[source]
    
    return total_emissions / 1000  # Convert to tonnes

def calculate_economic_impact(load_shedding_hours: float, average_demand: float, 
                           tariff_rate: float) -> Dict[str, float]:
    """Calculate economic impact of load shedding"""
    lost_energy = load_shedding_hours * average_demand  # MWh
    lost_revenue = lost_energy * tariff_rate * 1000  # Convert to USD
    
    # Additional economic costs (productivity loss, equipment damage, etc.)
    productivity_loss = lost_revenue * 2.5  # 2.5x multiplier for indirect costs
    total_economic_impact = lost_revenue + productivity_loss
    
    return {
        'lost_energy_mwh': lost_energy,
        'lost_revenue_usd': lost_revenue,
        'productivity_loss_usd': productivity_loss,
        'total_impact_usd': total_economic_impact
    }

def optimize_renewable_integration(current_mix: Dict, target_renewable_share: float) -> Dict[str, float]:
    """Optimize renewable energy integration"""
    total_generation = sum(current_mix.values())
    current_renewable = current_mix.get('solar', 0) + current_mix.get('wind', 0)
    current_renewable_share = current_renewable / total_generation if total_generation > 0 else 0
    
    if current_renewable_share >= target_renewable_share:
        return current_mix
    
    # Calculate required renewable capacity
    required_renewable = total_generation * target_renewable_share
    additional_solar = required_renewable * 0.7  # 70% solar
    additional_wind = required_renewable * 0.3   # 30% wind
    
    optimized_mix = current_mix.copy()
    optimized_mix['solar'] = optimized_mix.get('solar', 0) + additional_solar
    optimized_mix['wind'] = optimized_mix.get('wind', 0) + additional_wind
    
    return optimized_mix

def calculate_grid_stability_metrics(frequency: float, voltage: float, 
                                    power_factor: float) -> Dict[str, str]:
    """Calculate grid stability metrics"""
    stability_status = {}
    
    # Frequency stability
    if 49.5 <= frequency <= 50.5:
        stability_status['frequency'] = 'STABLE'
    elif 49.0 <= frequency <= 51.0:
        stability_status['frequency'] = 'MARGINAL'
    else:
        stability_status['frequency'] = 'UNSTABLE'
    
    # Voltage stability
    voltage_deviation = abs(voltage - 33.0) / 33.0 * 100
    if voltage_deviation <= 5:
        stability_status['voltage'] = 'STABLE'
    elif voltage_deviation <= 10:
        stability_status['voltage'] = 'MARGINAL'
    else:
        stability_status['voltage'] = 'UNSTABLE'
    
    # Power factor
    if power_factor >= 0.95:
        stability_status['power_factor'] = 'EXCELLENT'
    elif power_factor >= 0.90:
        stability_status['power_factor'] = 'GOOD'
    else:
        stability_status['power_factor'] = 'POOR'
    
    return stability_status

def format_energy_data(data: Dict) -> str:
    """Format energy data for display"""
    formatted = f"Energy Status Report\n"
    formatted += f"==================\n\n"
    formatted += f"Current Load: {data.get('current_load', 0):.1f} MW\n"
    formatted += f"Total Capacity: {data.get('total_capacity', 0):.1f} MW\n"
    formatted += f"Utilization: {data.get('utilization', 0):.1f}%\n"
    formatted += f"Reserve Margin: {data.get('reserve_margin', 0):.1f}%\n"
    formatted += f"Renewable Share: {data.get('renewable_share', 0):.1f}%\n"
    formatted += f"Risk Level: {data.get('risk_level', 'UNKNOWN')}\n"
    
    return formatted

def save_energy_data(data: Dict, filename: str = None) -> str:
    """Save energy data to JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"energy_data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    return filename

def load_energy_data(filename: str) -> Dict:
    """Load energy data from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def calculate_peak_demand_charge(consumption: float, demand_charge_rate: float) -> float:
    """Calculate peak demand charge for commercial/industrial customers"""
    return consumption * demand_charge_rate

def estimate_energy_savings(efficiency_measures: List[str]) -> Dict[str, float]:
    """Estimate energy savings from efficiency measures"""
    savings_estimates = {
        'led_lighting': 0.15,  # 15% savings
        'energy_efficient_appliances': 0.20,  # 20% savings
        'smart_thermostats': 0.10,  # 10% savings
        'insulation_improvements': 0.25,  # 25% savings
        'solar_water_heating': 0.30,  # 30% savings
        'power_factor_correction': 0.05,  # 5% savings
    }
    
    total_savings = 0
    for measure in efficiency_measures:
        if measure in savings_estimates:
            total_savings += savings_estimates[measure]
    
    return {
        'individual_savings': {measure: savings_estimates.get(measure, 0) 
                              for measure in efficiency_measures},
        'total_savings_percent': min(0.50, total_savings),  # Cap at 50%
        'estimated_annual_savings_mwh': 0  # To be calculated based on consumption
    }

def create_energy_report(data: Dict) -> str:
    """Create comprehensive energy report"""
    report = f"Zambia Energy Management Report\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"{'='*50}\n\n"
    
    # System Status
    report += f"System Status:\n"
    report += f"- Current Load: {data.get('current_load', 0):.1f} MW\n"
    report += f"- Grid Utilization: {data.get('utilization', 0):.1f}%\n"
    report += f"- Risk Level: {data.get('risk_level', 'UNKNOWN')}\n\n"
    
    # Load Shedding
    if data.get('load_shedding_schedule'):
        report += f"Load Shedding Schedule:\n"
        for entry in data['load_shedding_schedule']:
            report += f"- {entry['zone']}: {entry['duration']} hours\n"
        report += "\n"
    
    # Recommendations
    if data.get('recommendations'):
        report += f"Recommendations:\n"
        for i, rec in enumerate(data['recommendations'], 1):
            report += f"{i}. {rec}\n"
    
    return report

