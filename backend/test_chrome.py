"""
Test Chrome/ChromeDriver setup to ensure web scraping functionality works
Updated for legal document scraping sources
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_chrome_setup():
    """Test Chrome and ChromeDriver functionality for legal document scraping"""
    driver = None
    try:
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Create driver
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        logger.info("✅ Chrome WebDriver created successfully")
        
        # Test basic navigation
        driver.get("https://www.google.com")
        logger.info("✅ Successfully navigated to Google")
        
        # Test element finding
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("legal documents court cases")
        logger.info("✅ Successfully interacted with page elements")
        
        # Test legal document source access
        test_sources = [
            ("CourtListener", "https://www.courtlistener.com"),
            ("Justia", "https://law.justia.com"),
            ("Cornell Law", "https://www.law.cornell.edu")
        ]
        
        for source_name, url in test_sources:
            try:
                driver.get(url)
                time.sleep(3)
                
                title = driver.title
                logger.info(f"✅ Successfully accessed {source_name}. Title: {title}")
                
            except Exception as e:
                logger.warning(f"⚠️  Could not access {source_name}: {e}")
        
        logger.info("🎉 Chrome/ChromeDriver setup test completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Chrome setup test failed: {e}")
        return False
    finally:
        if driver:
            driver.quit()
            logger.info("🔒 Chrome driver closed")

def test_api_connectivity():
    """Test connectivity to legal document APIs"""
    try:
        logger.info("🌐 Testing API connectivity...")
        
        # Test APIs that don't require authentication
        test_apis = [
            ("Congress.gov API", "https://api.congress.gov/v3"),
            ("Federal Register API", "https://www.federalregister.gov/api/v1"),
            ("CourtListener API", "https://www.courtlistener.com/api/rest/v3")
        ]
        
        for api_name, api_url in test_apis:
            try:
                response = requests.get(api_url, timeout=10)
                if response.status_code in [200, 403, 404]:  # 403/404 expected without auth
                    logger.info(f"✅ {api_name} is reachable (Status: {response.status_code})")
                else:
                    logger.warning(f"⚠️  {api_name} returned status {response.status_code}")
            except requests.RequestException as e:
                logger.warning(f"⚠️  Could not reach {api_name}: {e}")
        
        logger.info("🌐 API connectivity test completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ API connectivity test failed: {e}")
        return False

def test_parsing_capabilities():
    """Test HTML parsing capabilities for legal documents"""
    try:
        logger.info("📄 Testing HTML parsing capabilities...")
        
        from bs4 import BeautifulSoup
        import lxml
        
        # Test HTML parsing
        sample_html = """
        <html>
            <body>
                <div class="case-title">Sample v. Legal Case</div>
                <div class="court-name">Supreme Court</div>
                <div class="date">2024-01-15</div>
                <div class="citation">123 U.S. 456 (2024)</div>
            </body>
        </html>
        """
        
        soup = BeautifulSoup(sample_html, 'lxml')
        
        # Test element extraction
        title = soup.select_one('.case-title')
        court = soup.select_one('.court-name')
        date = soup.select_one('.date')
        citation = soup.select_one('.citation')
        
        if all([title, court, date, citation]):
            logger.info("✅ HTML parsing working correctly")
            logger.info(f"   📋 Extracted: {title.text}, {court.text}, {date.text}, {citation.text}")
            return True
        else:
            logger.error("❌ HTML parsing failed")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Missing parsing dependencies: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Parsing test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests for legal document scraping setup"""
    logger.info("🎯 Starting Comprehensive Legal Document Scraping Setup Test")
    logger.info("=" * 60)
    
    tests = [
        ("Chrome WebDriver Setup", test_chrome_setup),
        ("API Connectivity", test_api_connectivity),
        ("HTML Parsing Capabilities", test_parsing_capabilities)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running: {test_name}")
        logger.info("-" * 40)
        
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"❌ Test {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} {test_name}")
    
    logger.info(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! System ready for legal document scraping.")
        return True
    else:
        logger.warning("⚠️  Some tests failed. Please review issues above.")
        return False

if __name__ == "__main__":
    print("🎯 Legal Document Scraping - Chrome & System Test")
    print("=" * 60)
    
    success = run_comprehensive_test()
    
    if success:
        print("\n✅ Setup test completed successfully!")
        print("🚀 Ready to implement legal document scraping!")
    else:
        print("\n❌ Setup test failed!")
        print("🔧 Please fix the issues above before proceeding.")