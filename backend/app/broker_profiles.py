"""
Data Broker Profile Sets for Targeted Discovery

This module defines logical groupings of data brokers to enable faster,
more targeted privacy discovery scans instead of searching all 658+ brokers.
"""

from typing import Dict, List, Any

# High-priority broker domains for each profile
BROKER_PROFILES: Dict[str, Dict[str, Any]] = {
        "quick_scan": {
        "name": "Quick Essential Scan",
        "description": "Top 15 high-priority data brokers for immediate results",
        "priority": 5,
        "estimated_time": "15 minutes",
        "broker_count": 15,
        "color": "#10b981",
        "icon": "⚡",
        "brokers": [
            # Start with most reliable, fastest sites
            "spokeo.com", "whitepages.com", "truepeoplesearch.com", 
            "freepeoplesearch.com", "peoplewhiz.com", "checkpeople.com",
            "usinfosearch.com", "publicdatacheck.com", "searchpublicrecords.com",
            "instantcheckmate.com", "peoplefinders.com", "privaterecords.net",
            "peopledatalabs.com", "intelius.com", 
            # Put slower sites last
            "beenverified.com"
        ]
    },
    
    "people_search": {
        "name": "High-Impact People Search",
        "description": "Major people search engines and background check services",
        "priority": 5,
        "estimated_time": "30 minutes",
        "broker_count": 28,
        "color": "#4ecdc4",
        "icon": "🔍",
        "brokers": [
            # Major people search platforms
            "spokeo.com", "whitepages.com", "intelius.com", "truthfinder.com",
            "beenverified.com", "instantcheckmate.com", "peoplefinders.com",
            
            # Free people search sites
            "freepeoplesearch.com", "truepeoplesearch.com", "peoplesearcher.com",
            "fastpeoplesearch.com", "openpeoplesearch.com", "uspeoplesearch.com",
            "advancedbackgroundchecks.com", "checkpeople.com",
            
            # Background check services
            "backgroundchecks.com", "checkthem.com", "goodhire.com",
            "hireright.com", "sterlingcheck.com",
            
            # Public records
            "publicrecords.com", "familytreenow.com", "zabasearch.com",
            "radaris.com", "pipl.com", "thatsthem.com", "addresses.com",
            "411.com"
        ]
    },
    
    "financial_credit": {
        "name": "Financial & Credit Services", 
        "description": "Credit bureaus, financial services, and credit monitoring companies",
        "priority": 5,
        "estimated_time": "45 minutes",
        "broker_count": 35,
        "color": "#45b7d1",
        "icon": "💳",
        "brokers": [
            # Credit bureaus & reporting
            "acxiom.com", "experian.com", "equifax.com", "transunion.com",
            "700credit.com", "ciccredit.com", "theworknumber.com",
            
            # Financial data companies
            "sagestreamllc.com", "partnerscredit.com", "innovis.com",
            "chexsystems.com", "earlywarning.com", "lexisnexis.com",
            
            # Credit monitoring & identity
            "creditkarma.com", "creditsesame.com", "quizzle.com",
            "freecreditscore.com", "myfico.com", "identityguard.com",
            
            # Financial services data
            "corelogic.com", "firstam.com", "blackknight.com",
            "epsilon.com", "merkle.com", "alliant.com",
            
            # Banking & lending data
            "bankrate.com", "lendingtree.com", "nerdwallet.com",
            "creditcards.com", "insurance.com", "quotewizard.com",
            
            # Investment & wealth data
            "wealthx.com", "morningstar.com", "refinitiv.com",
            "factset.com", "bloomberg.com"
        ]
    },
    
    "marketing_advertising": {
        "name": "Marketing & Advertising Networks",
        "description": "Ad networks, marketing data companies, and lead generation services", 
        "priority": 4,
        "estimated_time": "90 minutes",
        "broker_count": 95,
        "color": "#96ceb4",
        "icon": "📢",
        "brokers": [
            # Major data marketing companies
            "acxiom.com", "epsilon.com", "experian.com", "merkle.com",
            "alliant.com", "analyticsiq.com", "liveramp.com",
            
            # Lead generation companies
            "bookyourdata.com", "addirectinc.com", "awl.com", "calibrant.com",
            "homeownersmarketingservices.com", "4legalleads.com",
            
            # Digital advertising networks
            "33across.com", "adsquare.com", "audigent.com", "beeswax.com",
            "liveramp.com", "lotame.com", "neustar.com", "oracle.com",
            
            # Marketing automation
            "salesforce.com", "hubspot.com", "marketo.com", "pardot.com",
            "eloqua.com", "constantcontact.com", "mailchimp.com",
            
            # Social media advertising
            "facebook.com", "instagram.com", "twitter.com", "linkedin.com",
            "pinterest.com", "snapchat.com", "tiktok.com", "youtube.com",
            
            # Programmatic advertising
            "thetradedesk.com", "adobe.com", "amazon.com", "google.com",
            "microsoft.com", "yahoo.com", "verizonmedia.com",
            
            # Direct marketing
            "usadata.com", "dunbradstreet.com", "hoovers.com", "leadspace.com",
            "zoominfo.com", "discoverorg.com", "salesintel.com",
            
            # Email marketing
            "validity.com", "returnpath.com", "sendgrid.com", "mailgun.com",
            "campaignmonitor.com", "aweber.com", "getresponse.com",
            
            # Analytics & tracking
            "google.com", "adobe.com", "salesforce.com", "segment.com",
            "mixpanel.com", "amplitude.com", "heap.com", "fullstory.com",
            
            # Media & publishing
            "acbj.com", "gannett.com", "hearst.com", "meredith.com",
            "timesinc.com", "washpost.com", "nytimes.com",
            
            # Additional marketing services
            "datalogix.com", "axciom.com", "polk.com", "claritas.com",
            "simmons.com", "mri.com", "comscore.com", "nielsen.com",
            "kantar.com", "ipsos.com", "gfk.com", "harris.com",
            "yougov.com", "surveymonkey.com", "qualtrics.com"
        ]
    },
    
    "real_estate_property": {
        "name": "Real Estate & Property Data",
        "description": "Property records, real estate marketing, and home services data",
        "priority": 3,
        "estimated_time": "35 minutes", 
        "broker_count": 25,
        "color": "#f7dc6f",
        "icon": "🏠",
        "brokers": [
            # Property data companies
            "propertyradar.com", "propertyreach.com", "attomdata.com",
            "corelogic.com", "firstam.com", "blackknight.com",
            
            # Real estate platforms
            "zillow.com", "redfin.com", "realtor.com", "trulia.com",
            "homes.com", "homesnap.com", "crexi.com",
            
            # Home services & leads
            "homedata.com", "homeownersmarketingservices.com",
            "homeservicescompliance.com", "solarpower-experts.com",
            "remodeling.com", "angi.com", "thumbtack.com",
            
            # Property records & title
            "publicrecords.com", "realquest.com", "dataree.com",
            "titlepoint.com", "landwatch.com", "loopnet.com",
            
            # Additional property services
            "factualdata.com", "buildertrend.com"
        ]
    },
    
    "healthcare_medical": {
        "name": "Healthcare & Medical Data",
        "description": "Medical data companies, healthcare marketing, and wellness services",
        "priority": 5,
        "estimated_time": "25 minutes",
        "broker_count": 18,
        "color": "#e74c3c",
        "icon": "🏥", 
        "brokers": [
            # Medical data companies
            "completemedicallists.com", "healthwisedata.com",
            "integratedmedicaldata.com", "healthlinkdimensions.com",
            
            # Healthcare analytics
            "komodohealth.com", "monocl.com", "definitivehc.com",
            "iqvia.com", "veracyte.com", "flatiron.com",
            
            # Medicare & insurance
            "pickmedicare.com", "healthcare.com", "benefitfocus.com",
            "gohealth.com", "selectquote.com",
            
            # Health & wellness marketing
            "healthiswealthmedicare.com", "welldyne.com",
            "cvs.com", "walgreens.com", "express-scripts.com"
        ]
    },
    
    "professional_b2b": {
        "name": "Professional & B2B Services",
        "description": "Business data, professional networks, and B2B lead generation",
        "priority": 3,
        "estimated_time": "70 minutes",
        "broker_count": 55,
        "color": "#9b59b6",
        "icon": "💼",
        "brokers": [
            # Major B2B data platforms
            "zoominfo.com", "apollo.io", "amplemarket.com", "6sense.com",
            "salesforce.com", "hubspot.com", "outreach.io", "salesloft.com",
            
            # Professional networks & data
            "linkedin.com", "xing.com", "viadeo.com", "indeed.com",
            "glassdoor.com", "monster.com", "careerbuilder.com",
            
            # Business intelligence
            "hoovers.com", "dunbradstreet.com", "bisnode.com",
            "creditsafe.com", "experian.com", "equifax.com",
            
            # Lead generation & sales
            "leadspace.com", "discoverorg.com", "salesintel.com",
            "uplead.com", "lusha.com", "rocketreach.com", "hunter.io",
            
            # Legal & professional services
            "aristotle.com", "4legalleads.com", "martindale.com",
            "avvo.com", "lawyers.com", "findlaw.com",
            
            # Business directories
            "yellowpages.com", "superpages.com", "yelp.com",
            "bbb.org", "manta.com", "bizapedia.com",
            
            # Industry-specific platforms
            "thomasnet.com", "globalspec.com", "engineering.com",
            "meddeviceonline.com", "bioworld.com", "fiercepharma.com",
            
            # Conference & events
            "eventbrite.com", "meetup.com", "cvent.com",
            "bizzabo.com", "attendify.com",
            
            # Additional B2B services
            "marketo.com", "pardot.com", "eloqua.com", "constantcontact.com",
            "mailchimp.com", "campaignmonitor.com", "sendgrid.com"
        ]
    },
    
    "tech_data_analytics": {
        "name": "Tech & Data Analytics", 
        "description": "Technology companies, data analytics platforms, and AI/ML services",
        "priority": 2,
        "estimated_time": "120 minutes",
        "broker_count": 85,
        "color": "#34495e",
        "icon": "🤖",
        "brokers": [
            # Major tech platforms
            "google.com", "microsoft.com", "amazon.com", "apple.com",
            "facebook.com", "twitter.com", "linkedin.com", "oracle.com",
            
            # Data analytics companies
            "analyticsiq.com", "palantir.com", "snowflake.com",
            "databricks.com", "tableau.com", "looker.com", "qlik.com",
            
            # AI/ML platforms
            "openai.com", "anthropic.com", "cohere.ai", "stability.ai",
            "huggingface.co", "scale.ai", "dataiku.com", "h2o.ai",
            
            # Cloud data services
            "aws.amazon.com", "azure.microsoft.com", "cloud.google.com",
            "digitalocean.com", "cloudflare.com", "fastly.com",
            
            # Data management platforms
            "segment.com", "rudderstack.com", "fivetran.com",
            "stitch.com", "airbyte.io", "census.dev", "hightouch.io",
            
            # Analytics & tracking
            "mixpanel.com", "amplitude.com", "heap.com", "fullstory.com",
            "hotjar.com", "crazyegg.com", "optimizely.com", "split.io",
            
            # Data enrichment
            "clearbit.com", "peopledatalabs.com", "pipl.com",
            "fullcontact.com", "whitepages.com", "melissa.com",
            
            # Business intelligence
            "looker.com", "sisense.com", "domo.com", "chartio.com",
            "metabase.com", "grafana.com", "kibana.com",
            
            # Additional tech services
            "twilio.com", "stripe.com", "plaid.com", "yodlee.com",
            "intuit.com", "quickbooks.com", "xero.com", "freshworks.com",
            "zendesk.com", "intercom.com", "drift.com", "calendly.com",
            "zoom.com", "slack.com", "dropbox.com", "box.com",
            "github.com", "gitlab.com", "atlassian.com", "notion.so",
            "airtable.com", "monday.com", "asana.com", "trello.com"
        ]
    },
    
    "all_brokers": {
        "name": "Complete Comprehensive Scan",
        "description": "All 658 data brokers - most thorough but time-intensive scan",
        "priority": 1,
        "estimated_time": "10+ hours",
        "broker_count": 658,
        "color": "#7f8c8d",
        "icon": "🌐",
        "brokers": []  # Empty means all brokers
    }
}


def get_broker_profiles() -> Dict[str, Dict[str, Any]]:
    """Get all available broker profiles."""
    return BROKER_PROFILES


def get_profile_by_name(profile_name: str) -> Dict[str, Any]:
    """Get a specific broker profile by name."""
    if profile_name not in BROKER_PROFILES:
        raise ValueError(f"Unknown broker profile: {profile_name}")
    return BROKER_PROFILES[profile_name]


def filter_brokers_by_profile(all_brokers: List[Dict], profile_name: str) -> List[Dict]:
    """Filter broker list by profile name, maintaining the order specified in the profile."""
    if profile_name == "all_brokers" or profile_name not in BROKER_PROFILES:
        return all_brokers
    
    profile = BROKER_PROFILES[profile_name]
    profile_domains = profile["brokers"]  # Keep as list to preserve order
    
    # Create a mapping from domain to broker data
    broker_map = {broker.get("domain"): broker for broker in all_brokers}
    
    # Filter and order brokers according to profile specification
    filtered_brokers = []
    for domain in profile_domains:
        if domain in broker_map:
            filtered_brokers.append(broker_map[domain])
    
    return filtered_brokers


def get_profile_recommendations(user_concerns: List[str] = None) -> List[str]:
    """Recommend broker profiles based on user concerns."""
    if not user_concerns:
        return ["quick_scan", "people_search", "financial_credit"]
    
    recommendations = ["quick_scan"]  # Always recommend quick scan first
    
    concern_mapping = {
        "financial_privacy": "financial_credit",
        "online_presence": "people_search", 
        "marketing_emails": "marketing_advertising",
        "property_records": "real_estate_property",
        "medical_privacy": "healthcare_medical",
        "professional_reputation": "professional_b2b",
        "data_analytics": "tech_data_analytics"
    }
    
    for concern in user_concerns:
        if concern in concern_mapping:
            profile = concern_mapping[concern]
            if profile not in recommendations:
                recommendations.append(profile)
    
    return recommendations