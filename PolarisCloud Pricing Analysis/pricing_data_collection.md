# GPU Cloud Pricing Data Collection Guide

## Step-by-Step Data Collection Process

### 1. RunPod Pricing Research

**Website**: https://www.runpod.io/pricing

**Data to Collect**:
- RTX 4090 pricing (hourly/monthly)
- A100 40GB pricing
- A100 80GB pricing  
- H100 pricing
- Spot vs on-demand rates
- Storage costs
- Network/bandwidth costs
- Support tiers and costs

**Collection Steps**:
1. Visit RunPod pricing page
2. Screenshot current pricing table
3. Note any promotional offers or discounts
4. Check for enterprise pricing (if available)
5. Document minimum commitment requirements

**Expected GPU Types**:
- RTX 4090: ~$0.50-1.00/hour
- A100 40GB: ~$1.50-3.00/hour
- A100 80GB: ~$2.00-4.00/hour
- H100: ~$3.00-6.00/hour

### 2. Vast.ai Pricing Research

**Website**: https://vast.ai/pricing

**Data to Collect**:
- Current market rates for different GPUs
- Spot pricing availability
- Minimum and maximum rates
- Additional fees (storage, network)
- User rating requirements

**Collection Steps**:
1. Visit Vast.ai pricing page
2. Check current market rates
3. Note price ranges for each GPU type
4. Document any additional costs
5. Check for bulk pricing options

**Expected GPU Types**:
- RTX 4090: ~$0.20-0.80/hour (spot pricing)
- A100 40GB: ~$0.80-2.50/hour
- A100 80GB: ~$1.20-3.50/hour
- H100: ~$2.00-5.00/hour

### 3. Lambda Labs Pricing Research

**Website**: https://lambda.ai/pricing

**Data to Collect**:
- GPU instance pricing
- Monthly subscription options
- Enterprise pricing tiers
- Storage and network costs
- Support levels and pricing

**Collection Steps**:
1. Visit Lambda Labs pricing page
2. Check both hourly and monthly rates
3. Note enterprise vs individual pricing
4. Document support tier costs
5. Check for educational discounts

**Expected GPU Types**:
- RTX 4090: ~$0.80-1.50/hour
- A100 40GB: ~$2.00-4.00/hour
- A100 80GB: ~$3.00-5.00/hour
- H100: ~$4.00-8.00/hour

### 4. PolarisCloud Current Pricing

**Website**: https://polariscloud.ai/pricing

**Data to Collect**:
- Current tier specifications
- Current pricing (ignore for new pricing strategy)
- Service features and support levels
- Hardware specifications for each tier
- Additional services and costs

**Collection Steps**:
1. Visit PolarisCloud pricing page
2. Document current tier structure
3. Note hardware specifications
4. Document service features
5. Check for any current promotional pricing

### 5. Data Collection Template

Use this template for each provider:

```
Provider: [Name]
Date Collected: [Date]
Website: [URL]

GPU Type | Hourly Rate | Monthly Rate | Spot Rate | Storage Cost | Network Cost | Support Level
---------|-------------|-------------|-----------|--------------|--------------|---------------
RTX 4090 | $X.XX      | $XXX.XX     | $X.XX     | $X.XX/GB    | $X.XX/GB     | [Level]
A100 40GB| $X.XX      | $XXX.XX     | $X.XX     | $X.XX/GB    | $X.XX/GB     | [Level]
A100 80GB| $X.XX      | $XXX.XX     | $X.XX     | $X.XX/GB    | $X.XX/GB     | [Level]
H100     | $X.XX      | $XXX.XX     | $X.XX     | $X.XX/GB    | $X.XX/GB     | [Level]

Additional Notes:
- [Any special pricing or conditions]
- [Minimum commitments]
- [Educational discounts]
- [Enterprise features]
```

### 6. Monthly Cost Calculation Formula

```
Monthly Cost = Hourly Rate × 730 hours (average month)
Total Monthly Cost = Monthly Cost + Storage Cost + Network Cost + Support Cost
```

### 7. Verification Steps

**Cross-Reference Data**:
1. Check multiple sources for the same pricing
2. Verify calculations with online calculators
3. Compare with industry benchmarks
4. Note any discrepancies or special conditions

**Data Quality Checks**:
- Are prices current (within last 30 days)?
- Are all fees included in calculations?
- Are spot vs on-demand clearly differentiated?
- Are enterprise vs individual pricing noted?

### 8. Data Storage

**File Organization**:
```
pricing_data/
├── runpod_pricing_[date].csv
├── vast_ai_pricing_[date].csv
├── lambda_labs_pricing_[date].csv
├── polariscloud_current_[date].csv
├── screenshots/
│   ├── runpod_screenshot_[date].png
│   ├── vast_ai_screenshot_[date].png
│   ├── lambda_labs_screenshot_[date].png
│   └── polariscloud_screenshot_[date].png
└── raw_data/
    ├── runpod_raw_[date].txt
    ├── vast_ai_raw_[date].txt
    ├── lambda_labs_raw_[date].txt
    └── polariscloud_raw_[date].txt
```

### 9. Update Schedule

**Regular Updates**:
- Weekly: Check for pricing changes
- Monthly: Full data refresh
- Quarterly: Comprehensive analysis update
- Before major pricing decisions: Immediate verification

### 10. Quality Assurance

**Data Validation**:
- Screenshot all pricing pages for verification
- Document collection date and time
- Note any special conditions or limitations
- Cross-check calculations
- Verify currency and units

**Common Pitfalls to Avoid**:
- Mixing spot and on-demand pricing
- Forgetting additional fees
- Using outdated pricing
- Not accounting for minimum commitments
- Ignoring regional pricing differences

## Next Steps After Data Collection

1. **Data Processing**: Clean and standardize collected data
2. **Analysis**: Calculate savings percentages and competitive positioning
3. **Visualization**: Create charts and graphs for presentation
4. **Recommendations**: Develop pricing strategy suggestions
5. **Monitoring**: Set up regular data collection schedule

