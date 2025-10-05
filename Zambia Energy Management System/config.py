#!/usr/bin/env python3
"""
Configuration file for Zambia Energy Management System
====================================================

This file contains all configurable parameters for the energy management system.
Modify these settings to customize the system for Zambia's specific energy needs.
"""

# Zambian Power Grid Configuration
POWER_GRID_CONFIG = {
    'total_capacity_mw': 2890,  # Total installed capacity in MW
    'peak_demand_mw': 2500,    # Peak demand in MW
    'base_load_mw': 1500,      # Base load in MW
    'reserve_margin_percent': 15,  # Reserve margin percentage
    'transmission_losses_percent': 8,  # Transmission and distribution losses
}

# Zambian Power Stations
POWER_STATIONS = {
    'Kafue Gorge': {
        'capacity_mw': 990,
        'type': 'hydro',
        'status': 'operational',
        'location': 'Southern Province',
        'commissioned': 1972,
        'efficiency': 0.85
    },
    'Kariba North': {
        'capacity_mw': 1080,
        'type': 'hydro',
        'status': 'operational',
        'location': 'Southern Province',
        'commissioned': 1977,
        'efficiency': 0.88
    },
    'Itezhi-Tezhi': {
        'capacity_mw': 120,
        'type': 'hydro',
        'status': 'operational',
        'location': 'Central Province',
        'commissioned': 2016,
        'efficiency': 0.82
    },
    'Lusaka West': {
        'capacity_mw': 300,
        'type': 'thermal',
        'status': 'operational',
        'location': 'Lusaka Province',
        'commissioned': 2016,
        'efficiency': 0.35
    },
    'Copperbelt Energy': {
        'capacity_mw': 200,
        'type': 'thermal',
        'status': 'operational',
        'location': 'Copperbelt Province',
        'commissioned': 2000,
        'efficiency': 0.38
    },
    'Solar Farms': {
        'capacity_mw': 150,
        'type': 'solar',
        'status': 'operational',
        'location': 'Multiple',
        'commissioned': 2020,
        'efficiency': 0.20
    },
    'Wind Farms': {
        'capacity_mw': 50,
        'type': 'wind',
        'status': 'operational',
        'location': 'Eastern Province',
        'commissioned': 2021,
        'efficiency': 0.35
    }
}

# Load Shedding Zones in Zambia
LOAD_SHEDDING_ZONES = {
    'Lusaka': {
        'population': 3000000,
        'priority': 'high',
        'average_demand_mw': 800,
        'peak_demand_mw': 1200,
        'load_shedding_hours_per_week': 8
    },
    'Kitwe': {
        'population': 500000,
        'priority': 'high',
        'average_demand_mw': 300,
        'peak_demand_mw': 450,
        'load_shedding_hours_per_week': 6
    },
    'Ndola': {
        'population': 500000,
        'priority': 'high',
        'average_demand_mw': 250,
        'peak_demand_mw': 375,
        'load_shedding_hours_per_week': 6
    },
    'Livingstone': {
        'population': 200000,
        'priority': 'medium',
        'average_demand_mw': 100,
        'peak_demand_mw': 150,
        'load_shedding_hours_per_week': 12
    },
    'Chipata': {
        'population': 150000,
        'priority': 'medium',
        'average_demand_mw': 80,
        'peak_demand_mw': 120,
        'load_shedding_hours_per_week': 10
    },
    'Kabwe': {
        'population': 200000,
        'priority': 'medium',
        'average_demand_mw': 120,
        'peak_demand_mw': 180,
        'load_shedding_hours_per_week': 8
    },
    'Chingola': {
        'population': 150000,
        'priority': 'low',
        'average_demand_mw': 90,
        'peak_demand_mw': 135,
        'load_shedding_hours_per_week': 15
    },
    'Mufulira': {
        'population': 100000,
        'priority': 'low',
        'average_demand_mw': 60,
        'peak_demand_mw': 90,
        'load_shedding_hours_per_week': 18
    }
}

# Load Shedding Configuration
LOAD_SHEDDING_CONFIG = {
    'high_risk_threshold': 0.95,  # 95% capacity utilization
    'medium_risk_threshold': 0.85,  # 85% capacity utilization
    'low_risk_threshold': 0.75,   # 75% capacity utilization
    'immediate_shedding_zones': ['Lusaka', 'Kitwe', 'Ndola'],
    'scheduled_shedding_zones': ['Livingstone', 'Chipata', 'Kabwe'],
    'emergency_shedding_zones': ['Chingola', 'Mufulira'],
    'minimum_shedding_duration_hours': 1,
    'maximum_shedding_duration_hours': 8,
    'notification_advance_hours': 2
}

# Energy Optimization Settings
OPTIMIZATION_CONFIG = {
    'peak_shaving_enabled': True,
    'demand_response_enabled': True,
    'renewable_integration_target': 0.30,  # 30% renewable by 2030
    'energy_efficiency_target': 0.20,  # 20% efficiency improvement
    'smart_grid_enabled': True,
    'battery_storage_capacity_mw': 100,
    'grid_stabilization_enabled': True
}

# Monitoring and Alert Settings
MONITORING_CONFIG = {
    'update_interval_seconds': 5,
    'data_retention_days': 30,
    'alert_thresholds': {
        'high_demand': 0.90,
        'low_reserve': 0.10,
        'transmission_loss': 0.12
    },
    'notification_channels': ['email', 'sms', 'dashboard'],
    'reporting_frequency': 'daily'
}

# Zambian Energy Policy Targets
ENERGY_POLICY_TARGETS = {
    'renewable_energy_target_2030': 0.30,  # 30% renewable by 2030
    'energy_access_target': 0.95,  # 95% electrification by 2030
    'energy_efficiency_improvement': 0.20,  # 20% efficiency improvement
    'grid_modernization_budget_usd': 500000000,  # $500M for grid modernization
    'renewable_investment_usd': 200000000,  # $200M for renewable energy
}

# Weather and Seasonal Factors
SEASONAL_CONFIG = {
    'dry_season_months': [4, 5, 6, 7, 8, 9, 10],  # April to October
    'wet_season_months': [11, 12, 1, 2, 3],  # November to March
    'hydro_generation_factor_dry': 0.7,  # 70% of capacity in dry season
    'hydro_generation_factor_wet': 1.0,  # 100% of capacity in wet season
    'solar_generation_factor_dry': 1.0,  # 100% of capacity in dry season
    'solar_generation_factor_wet': 0.8,  # 80% of capacity in wet season
    'temperature_impact_factor': 0.02,  # 2% increase per degree above 25°C
}

# Economic Factors
ECONOMIC_CONFIG = {
    'electricity_tariff_residential': 0.12,  # $0.12 per kWh
    'electricity_tariff_commercial': 0.15,  # $0.15 per kWh
    'electricity_tariff_industrial': 0.10,  # $0.10 per kWh
    'load_shedding_cost_per_mwh': 50,  # $50 per MWh lost due to load shedding
    'renewable_energy_feed_in_tariff': 0.08,  # $0.08 per kWh for renewable energy
    'carbon_tax_per_tonne': 25,  # $25 per tonne of CO2
}

# Grid Stability Parameters
GRID_STABILITY_CONFIG = {
    'frequency_standard_hz': 50.0,
    'frequency_tolerance_hz': 0.5,
    'voltage_standard_kv': 33.0,
    'voltage_tolerance_percent': 5.0,
    'power_factor_target': 0.95,
    'harmonics_limit_percent': 5.0
}

# Data Export Settings
EXPORT_CONFIG = {
    'data_format': 'json',  # json, csv, xml
    'compression_enabled': True,
    'encryption_enabled': False,
    'cloud_sync_enabled': False,
    'backup_frequency': 'daily',
    'retention_period_days': 365
}

# API Configuration
API_CONFIG = {
    'weather_api_key': None,  # Add weather API key for real-time weather data
    'grid_data_api_url': None,  # Add grid data API URL
    'notification_api_url': None,  # Add notification service API URL
    'rate_limit_requests_per_minute': 60,
    'timeout_seconds': 30
}

# User Interface Settings
UI_CONFIG = {
    'theme': 'dark',  # dark, light
    'language': 'en',  # en, zm (English, Zambian languages)
    'timezone': 'Africa/Lusaka',
    'date_format': '%Y-%m-%d',
    'time_format': '%H:%M:%S',
    'chart_update_interval_seconds': 10,
    'dashboard_refresh_interval_seconds': 30
}

