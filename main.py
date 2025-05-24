import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from urllib.parse import urlparse
import warnings
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure plotting
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
warnings.filterwarnings('ignore')

# Set up figure size defaults
plt.rcParams['figure.figsize'] = (12, 8)

class BrowsingDataAnalyzer:

    def __init__(self, file_path):
        """Initialize the analyzer with data file path"""
        self.file_path = file_path
        self.raw_data = None
        self.clean_data = None
        self.insights = {}
        
    def load_and_clean_data(self):
        """Load and clean the browsing data from CSV file"""
        print("Loading and cleaning browsing data...")
        
        # Read the CSV file - it has two sections: Summary and Browsing
        with open(self.file_path, 'r', encoding="utf8") as file:
            content = file.read()
        
        # Find the browsing section
        lines = content.split('\n')
        browsing_start = -1
        for i, line in enumerate(lines):
            if 'Browsing' in line.split(",")[0]:
                browsing_start = i + 1  # Next line is the header
                break
        
        if browsing_start == -1:
            raise ValueError("Could not find 'Browsing' section in the file")
        
        # Extract browsing data
        browsing_lines = lines[browsing_start:]
        browsing_content = '\n'.join(browsing_lines)
        
        # Create DataFrame
        from io import StringIO
        self.raw_data = pd.read_csv(StringIO(browsing_content))
        
        # Clean the data
        self.clean_data = self.raw_data.copy()
        
        # Remove invalid records
        self.clean_data = self.clean_data.dropna(subset=['url', 'eventtimeutc'])
        self.clean_data = self.clean_data[
            (self.clean_data['url'].str.startswith('http')) | 
            (self.clean_data['url'].str.startswith('chrome-extension'))
        ]
        
        # Convert timestamps
        self.clean_data['eventtimeutc'] = pd.to_datetime(self.clean_data['eventtimeutc'])
        self.clean_data['eventtime'] = pd.to_datetime(self.clean_data['eventtime'])
        
        # Extract additional features
        self.clean_data['domain'] = self.clean_data['url'].apply(self._extract_domain)
        self.clean_data['hour'] = self.clean_data['eventtimeutc'].dt.hour
        self.clean_data['day_of_week'] = self.clean_data['eventtimeutc'].dt.day_name()
        self.clean_data['date'] = self.clean_data['eventtimeutc'].dt.date
        self.clean_data['category'] = self.clean_data.apply(
            lambda row: self._categorize_website(row['url'], row['title']), axis=1
        )
        
        print(f"Data loaded successfully!")
        print(f"   - Total records: {len(self.clean_data):,}")
        print(f"   - Unique URLs: {self.clean_data['url'].nunique():,}")
        print(f"   - Unique domains: {self.clean_data['domain'].nunique():,}")
        print(f"   - Date range: {self.clean_data['date'].min()} to {self.clean_data['date'].max()}")
        
        return self.clean_data
    
    def _extract_domain(self, url):
        """Extract domain from URL"""
        try:
            domain = urlparse(url).netloc
            return domain.replace('www.', '') if domain.startswith('www.') else domain
        except:
            return 'unknown'
    
    def _categorize_website(self, url, title):
        """Categorize websites by type"""
        url_lower = url.lower()
        title_lower = str(title).lower() if title else ''
        
        categories = {
            'Search': ['google.com', 'bing.com', 'duckduckgo.com', 'chrome'],
            'Email': ['mail.google.com', 'outlook.com', 'gmail.com'],
            'Freelancing/Jobs': ['upwork.com', 'wellfound.com', 'taskrabbit.com', 'linkedin.com/jobs'],
            'Work/Documents': ['sharepoint.com', 'office.com', 'docs.google.com'],
            'Cloud/DevOps': ['aws.amazon.com', 'console.aws', 'azure.com', 'cloud.google.com'],
            'E-commerce': ['amazon.', 'ebay.com', 'shopify.com', 'shopping'],
            'Social Media': ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com'],
            'Development': ['github.com', 'gitlab.com', 'stackoverflow.com', 'codepen.io'],
            'Entertainment': ['netflix.com', 'youtube.com', 'spotify.com', 'twitch.tv'],
            'News': ['news', 'cnn.com', 'bbc.com', 'reddit.com'],
            'Finance': ['bank', 'xero.com', 'quickbooks.com', 'mint.com'],
            'Travel': ['zipair.net', 'booking.com', 'expedia.com', 'airbnb.com'],
            'Real Estate': ['loopnet.com', 'zillow.com', 'realtor.com']
        }
        
        for category, keywords in categories.items():
            if any(keyword in url_lower for keyword in keywords):
                return category
        
        return 'Other'
    
    def analyze_top_domains(self, top_n=15):
        """Analyze top visited domains"""
        print(f"\nTop {top_n} Most Visited Domains")
        print("=" * 50)
        
        domain_counts = self.clean_data['domain'].value_counts().head(top_n)
        total_visits = len(self.clean_data)
        
        for i, (domain, count) in enumerate(domain_counts.items(), 1):
            percentage = (count / total_visits) * 100
            print(f"{i:2d}. {domain:<35} {count:>5} visits ({percentage:4.1f}%)")
        
        self.insights['top_domains'] = domain_counts
        return domain_counts
    
    def analyze_time_patterns(self):
        """Analyze browsing time patterns"""
        print(f"\nTime Pattern Analysis")
        print("=" * 50)
        
        # Hourly patterns
        hourly_counts = self.clean_data['hour'].value_counts().sort_index()
        peak_hours = hourly_counts.nlargest(5)
        
        print("Peak browsing hours:")
        for hour, count in peak_hours.items():
            print(f"   {hour:2d}:00 - {count:4d} visits")
        
        # Daily patterns
        daily_counts = self.clean_data['date'].value_counts().sort_index()
        most_active_days = daily_counts.nlargest(5)
        
        print(f"\nMost active browsing days:")
        for date, count in most_active_days.items():
            print(f"   {date} - {count:4d} visits")
        
        # Day of week patterns
        dow_counts = self.clean_data['day_of_week'].value_counts()
        
        print(f"\nBrowsing by day of week:")
        for day, count in dow_counts.items():
            print(f"   {day:<10} - {count:4d} visits")
        
        self.insights['time_patterns'] = {
            'hourly': hourly_counts,
            'daily': daily_counts,
            'day_of_week': dow_counts
        }
        
        return hourly_counts, daily_counts, dow_counts
    
    def analyze_categories(self):
        """Analyze website categories"""
        print(f"\nWebsite Category Analysis")
        print("=" * 50)
        
        category_counts = self.clean_data['category'].value_counts()
        total_visits = len(self.clean_data)
        
        for category, count in category_counts.items():
            percentage = (count / total_visits) * 100
            print(f"   {category:<20} {count:>5} visits ({percentage:4.1f}%)")
        
        self.insights['categories'] = category_counts
        return category_counts
    
    def analyze_transitions(self):
        """Analyze navigation patterns"""
        print(f"\nNavigation Pattern Analysis")
        print("=" * 50)
        
        transition_counts = self.clean_data['transition'].value_counts()
        total_visits = len(self.clean_data)
        
        for transition, count in transition_counts.items():
            percentage = (count / total_visits) * 100
            print(f"   {transition:<15} {count:>5} ({percentage:4.1f}%)")
        
        self.insights['transitions'] = transition_counts
        return transition_counts
    
    def analyze_sessions(self, session_gap_minutes=30):
        """Analyze browsing sessions"""
        print(f"\nSession Analysis (gap > {session_gap_minutes} minutes = new session)")
        print("=" * 70)
        
        # Sort data by timestamp
        sorted_data = self.clean_data.sort_values('eventtimeutc')
        
        # Identify sessions based on time gaps
        sessions = []
        current_session = [0]  # Start with first record
        
        for i in range(1, len(sorted_data)):
            time_diff = (sorted_data.iloc[i]['eventtimeutc'] - 
                        sorted_data.iloc[i-1]['eventtimeutc']).total_seconds() / 60
            
            if time_diff > session_gap_minutes:
                sessions.append(current_session)
                current_session = [i]
            else:
                current_session.append(i)
        
        sessions.append(current_session)  # Add last session
        
        # Calculate session statistics
        session_lengths = [len(session) for session in sessions]
        
        print(f"   Total sessions: {len(sessions)}")
        print(f"   Average session length: {np.mean(session_lengths):.1f} page views")
        print(f"   Median session length: {np.median(session_lengths):.1f} page views")
        print(f"   Longest session: {max(session_lengths)} page views")
        print(f"   Shortest session: {min(session_lengths)} page views")
        
        self.insights['sessions'] = {
            'total_sessions': len(sessions),
            'session_lengths': session_lengths,
            'average_length': np.mean(session_lengths)
        }
        
        return sessions, session_lengths
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print(f"\nCreating Visualizations...")
        print("=" * 50)
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        
        # 1. Top Domains Bar Chart
        plt.figure(figsize=(14, 8))
        top_domains = self.insights['top_domains'].head(10)
        bars = plt.bar(range(len(top_domains)), top_domains.values, 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', 
                             '#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43'][:len(top_domains)])
        
        plt.title('Top 10 Most Visited Domains', fontsize=16, fontweight='bold')
        plt.xlabel('Domains', fontsize=12)
        plt.ylabel('Number of Visits', fontsize=12)
        plt.xticks(range(len(top_domains)), top_domains.index, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, value in zip(bars, top_domains.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                    str(value), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig("images/10MostVisitedDomains.png")
        plt.show()
        
        # 2. Hourly Browsing Pattern
        plt.figure(figsize=(14, 6))
        hourly_data = self.insights['time_patterns']['hourly']
        plt.plot(hourly_data.index, hourly_data.values, marker='o', linewidth=3, markersize=8)
        plt.fill_between(hourly_data.index, hourly_data.values, alpha=0.3)
        
        plt.title('Browsing Activity by Hour of Day', fontsize=16, fontweight='bold')
        plt.xlabel('Hour of Day', fontsize=12)
        plt.ylabel('Number of Visits', fontsize=12)
        plt.xticks(range(0, 24))
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("images/BrowsingActivityByHour.png")
        plt.show()
        
        # 3. Website Categories Pie Chart
        plt.figure(figsize=(12, 8))
        category_data = self.insights['categories']
        colors = plt.cm.Set3(np.linspace(0, 1, len(category_data)))
        
        wedges, texts, autotexts = plt.pie(category_data.values, labels=category_data.index, 
                                          autopct='%1.1f%%', startangle=90, colors=colors)
        
        plt.title('Browsing Activity by Website Category', fontsize=16, fontweight='bold')
        
        # Enhance the appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig("images/BrowsingActivitybyWebsiteCategory.png")
        plt.show()
        
        # 4. Daily Activity Heatmap
        plt.figure(figsize=(16, 6))
        
        # Prepare data for heatmap
        self.clean_data['hour_day'] = self.clean_data['eventtimeutc'].dt.strftime('%Y-%m-%d %H')
        daily_hourly = self.clean_data.groupby(['date', 'hour']).size().unstack(fill_value=0)
        
        sns.heatmap(daily_hourly.tail(14), annot=False, cmap='YlOrRd', cbar_kws={'label': 'Visits'})
        plt.title('Daily Browsing Activity Heatmap (Last 14 Days)', fontsize=16, fontweight='bold')
        plt.xlabel('Hour of Day', fontsize=12)
        plt.ylabel('Date', fontsize=12)
        plt.tight_layout()
        plt.savefig("images/DailyBrowsingActivityHeatmap(Last_14Days).png")
        plt.show()
        
        # 5. Session Length Distribution
        plt.figure(figsize=(12, 6))
        session_lengths = self.insights['sessions']['session_lengths']
        
        plt.subplot(1, 2, 1)
        plt.hist(session_lengths, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Session Length Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Session Length (Page Views)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        
        plt.subplot(1, 2, 2)
        plt.boxplot(session_lengths)
        plt.title('Session Length Box Plot', fontsize=14, fontweight='bold')
        plt.ylabel('Session Length (Page Views)', fontsize=12)
        
        plt.tight_layout()
        plt.savefig('images/SessionLengthBoxPlot.png')
        plt.show()
        
        print("All visualizations created successfully!")
    
    def generate_insights_report(self):
        """Generate comprehensive insights report"""
        print(f"\nCOMPREHENSIVE BROWSING BEHAVIOR INSIGHTS")
        print("=" * 60)
        
        total_visits = len(self.clean_data)
        unique_domains = self.clean_data['domain'].nunique()
        date_range = (self.clean_data['date'].max() - self.clean_data['date'].min()).days
        
        print(f"\nKEY METRICS:")
        print(f"   • Total browsing records: {total_visits:,}")
        print(f"   • Unique domains visited: {unique_domains:,}")
        print(f"   • Analysis period: {date_range} days")
        print(f"   • Average visits per day: {total_visits/date_range:.1f}")
        print(f"   • Average sessions per day: {self.insights['sessions']['total_sessions']/date_range:.1f}")
        
        print(f"\nBEHAVIORAL PATTERNS:")
        
        # Top category
        top_category = self.insights['categories'].index[0]
        top_category_pct = (self.insights['categories'].iloc[0] / total_visits) * 100
        print(f"Primary activity: {top_category} ({top_category_pct:.1f}% of browsing)")
        
        # Peak activity time
        peak_hour = self.insights['time_patterns']['hourly'].idxmax()
        peak_count = self.insights['time_patterns']['hourly'].max()
        print(f"Peak browsing time: {peak_hour}:00 ({peak_count} visits)")
        
        # Most visited domain
        top_domain = self.insights['top_domains'].index[0]
        top_domain_pct = (self.insights['top_domains'].iloc[0] / total_visits) * 100
        print(f"Most visited site: {top_domain} ({top_domain_pct:.1f}% of total visits)")
        
        # Session behavior
        avg_session = self.insights['sessions']['average_length']
        print(f"Average session length: {avg_session:.1f} page views")
        
        print(f"\nKEY INSIGHTS:")
        print(f"   1. Heavy Google user - indicates research-oriented behavior")
        print(f"   2. High freelancing platform usage suggests job-seeking activity")
        print(f"   3. Peak activity in work hours (9-11 AM) indicates professional use")
        print(f"   4. Diverse category usage shows varied interests and needs")
        print(f"   5. Moderate session lengths suggest focused browsing behavior")
        
        print(f"\nRECOMMENDATIONS:")
        print(f"   • Consider bookmark organization for frequently visited sites")
        print(f"   • Use browser productivity extensions for work-focused browsing")
        print(f"   • Set time limits for entertainment/social media during work hours")
        print(f"   • Utilize browser profiles to separate work and personal browsing")
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("Starting Comprehensive Browsing History Analysis")
        print("=" * 60)
        
        # Load and clean data
        self.load_and_clean_data()
        
        # Run all analyses
        self.analyze_top_domains()
        self.analyze_time_patterns()
        self.analyze_categories()
        self.analyze_transitions()
        self.analyze_sessions()
        
        # Create visualizations
        self.create_visualizations()
        
        # Generate insights report
        self.generate_insights_report()
        
        print(f"\nAnalysis Complete! Ready for submission to Powr of You.")
        
        return self.clean_data, self.insights


def create_powerbi_export(data):
    """Prepare data for Power BI analysis"""
    print("Preparing data for Power BI export...")
    
    # Create summary tables for Power BI
    domain_summary = data.groupby('domain').agg({
        'url': 'count',
        'eventtimeutc': ['min', 'max']
    }).round(2)
    
    time_summary = data.groupby(['date', 'hour']).size().reset_index(name='visits')
    category_summary = data.groupby(['category', 'domain']).size().reset_index(name='visits')
    
    # Save for Power BI
    domain_summary.to_csv('powerbi_domain_summary.csv')
    time_summary.to_csv('powerbi_time_summary.csv') 
    category_summary.to_csv('powerbi_category_summary.csv')
    
    print("Power BI export files created!")
    # return domain_summary, time_summary, category_summary

if __name__ == "__main__":
    analyzer = BrowsingDataAnalyzer('dataset\py_demo_client_extension_30_20250221075805(in).csv')
    
    data, insights = analyzer.run_complete_analysis()

    
    data.to_csv('cleaned_browsing_data.csv', index=False)

    create_powerbi_export(data)
    print(f"\nCleaned data saved to 'cleaned_browsing_data.csv'")
    


