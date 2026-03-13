import streamlit as st
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from analyzers import PythonAnalyzer, JavaAnalyzer, JavaScriptAnalyzer, CSharpAnalyzer
from utils.report_generator import ReportGenerator

st.set_page_config(
    page_title="Automation Code Verifier",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state for mode
if 'mode' not in st.session_state:
    st.session_state['mode'] = 'candidate'
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Password for Assessor Mode
ASSESSOR_PASSWORD = "radiant2026"

st.title("🔍 Automation Code Verifier")

# Mode selector in sidebar
with st.sidebar:
    st.title("🎯 Mode Selection")
    
    mode_selection = st.radio(
        "Select Mode:",
        options=["Candidate Mode", "Assessor Mode"],
        index=0 if st.session_state['mode'] == 'candidate' else 1
    )
    
    if mode_selection == "Candidate Mode":
        st.session_state['mode'] = 'candidate'
        st.session_state['authenticated'] = False
        st.info("📝 **Candidate Mode**\n\nWrite your Selenium automation code here. No analysis features available.")
    else:
        if not st.session_state['authenticated']:
            password_input = st.text_input("Enter Assessor Password:", type="password", key="password_input")
            if st.button("Unlock Assessor Mode"):
                if password_input == ASSESSOR_PASSWORD:
                    st.session_state['authenticated'] = True
                    st.session_state['mode'] = 'assessor'
                    st.success("✅ Authenticated! Assessor Mode unlocked.")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
        else:
            st.session_state['mode'] = 'assessor'
            st.success("✅ **Assessor Mode Active**\n\nFull analysis features available.")
            if st.button("Lock Assessor Mode"):
                st.session_state['authenticated'] = False
                st.session_state['mode'] = 'candidate'
                st.rerun()
    
    st.divider()

# Display mode-specific description
if st.session_state['mode'] == 'candidate':
    st.markdown("**✍️ Write your Selenium automation code below**")
else:
    st.markdown("**Analyze and verify Selenium automation code for issues and best practices**")

LANGUAGE_MAP = {
    "Python": {
        "analyzer": PythonAnalyzer,
        "lexer": "python",
        "example": """from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get("https://example.com")
    
    wait = WebDriverWait(driver, 10)
    element = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    
    element.send_keys("test_user")
    driver.find_element(By.ID, "submit").click()
    
finally:
    driver.quit()
"""
    },
    "Java": {
        "analyzer": JavaAnalyzer,
        "lexer": "java",
        "example": """import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;

public class SeleniumTest {
    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        
        try {
            driver.get("https://example.com");
            
            WebDriverWait wait = new WebDriverWait(driver, 10);
            wait.until(ExpectedConditions.presenceOfElementLocated(By.id("username")));
            
            driver.findElement(By.id("username")).sendKeys("test_user");
            driver.findElement(By.id("submit")).click();
            
        } finally {
            driver.quit();
        }
    }
}
"""
    },
    "JavaScript": {
        "analyzer": JavaScriptAnalyzer,
        "lexer": "javascript",
        "example": """const {Builder, By, until} = require('selenium-webdriver');

async function runTest() {
    let driver = await new Builder().forBrowser('chrome').build();
    
    try {
        await driver.get('https://example.com');
        
        await driver.wait(until.elementLocated(By.id('username')), 10000);
        
        await driver.findElement(By.id('username')).sendKeys('test_user');
        await driver.findElement(By.id('submit')).click();
        
    } finally {
        await driver.quit();
    }
}

runTest();
"""
    },
    "C#": {
        "analyzer": CSharpAnalyzer,
        "lexer": "csharp",
        "example": """using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;

class SeleniumTest 
{
    static void Main() 
    {
        IWebDriver driver = new ChromeDriver();
        
        try 
        {
            driver.Navigate().GoToUrl("https://example.com");
            
            WebDriverWait wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
            wait.Until(d => d.FindElement(By.Id("username")));
            
            driver.FindElement(By.Id("username")).SendKeys("test_user");
            driver.FindElement(By.Id("submit")).Click();
        } 
        finally 
        {
            driver.Quit();
        }
    }
}
"""
    }
}

# Language selection
if st.session_state['mode'] == 'candidate':
    col1, col2 = st.columns([2, 1])
    with col1:
        language = st.selectbox(
            "Select Programming Language",
            options=list(LANGUAGE_MAP.keys()),
            index=0
        )
    with col2:
        st.write("")
else:
    col1, col2 = st.columns([2, 1])
    with col1:
        language = st.selectbox(
            "Select Programming Language",
            options=list(LANGUAGE_MAP.keys()),
            index=0
        )
    with col2:
        if st.button("Load Example", use_container_width=True):
            st.session_state['code_input'] = LANGUAGE_MAP[language]['example']

code_input = st.text_area(
    "Enter your Selenium automation code:",
    height=400,
    value=st.session_state.get('code_input', ''),
    placeholder=f"Paste your {language} Selenium code here...",
    key='code_area'
)

# Mode-specific buttons
if st.session_state['mode'] == 'candidate':
    col_submit, col_clear = st.columns([3, 1])
    
    with col_submit:
        if st.button("📥 Download Code", type="primary", use_container_width=True):
            if code_input.strip():
                st.download_button(
                    label="💾 Save as .txt file",
                    data=code_input,
                    file_name=f"selenium_code_{language.lower()}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.warning("Please write some code first")
    
    with col_clear:
        if st.button("Clear", use_container_width=True):
            st.session_state['code_input'] = ''
            st.rerun()
    
    analyze_button = False
else:
    col_analyze, col_clear = st.columns([3, 1])
    
    with col_analyze:
        analyze_button = st.button("🔍 Analyze Code", type="primary", use_container_width=True)
    
    with col_clear:
        if st.button("Clear", use_container_width=True):
            st.session_state['code_input'] = ''
            st.rerun()

if analyze_button and code_input.strip():
    with st.spinner(f"Analyzing {language} code..."):
        analyzer_class = LANGUAGE_MAP[language]['analyzer']
        analyzer = analyzer_class(code_input)
        result = analyzer.analyze()
        
        st.divider()
        
        summary = result.get_summary()
        
        col_score, col_issues, col_critical, col_warnings, col_info = st.columns(5)
        
        with col_score:
            score_color = "green" if summary['score'] >= 80 else "orange" if summary['score'] >= 60 else "red"
            st.metric("Overall Score", f"{summary['score']}/100")
        
        with col_issues:
            st.metric("Total Issues", summary['total_issues'])
        
        with col_critical:
            st.metric("🔴 Critical", summary['critical'])
        
        with col_warnings:
            st.metric("⚠️ Warnings", summary['warnings'])
        
        with col_info:
            st.metric("ℹ️ Info", summary['info'])
        
        st.divider()
        
        if not result.syntax_valid:
            st.error(f"**Syntax Error:** {result.syntax_error}")
            st.warning("Fix syntax errors before proceeding with analysis.")
        else:
            if summary['total_issues'] == 0:
                st.success("🎉 **No issues found!** Your code looks great!")
            else:
                from analyzers.base import Issue
                
                critical_issues = result.get_issues_by_severity(Issue.CRITICAL)
                warning_issues = result.get_issues_by_severity(Issue.WARNING)
                info_issues = result.get_issues_by_severity(Issue.INFO)
                
                if critical_issues:
                    with st.expander(f"🔴 **CRITICAL ISSUES** ({len(critical_issues)})", expanded=True):
                        for issue in critical_issues:
                            st.markdown(f"**Line {issue.line}:** {issue.message}")
                            if issue.suggestion:
                                st.info(f"💡 {issue.suggestion}")
                            st.divider()
                
                if warning_issues:
                    with st.expander(f"⚠️ **WARNINGS** ({len(warning_issues)})", expanded=True):
                        for issue in warning_issues:
                            st.markdown(f"**Line {issue.line}:** {issue.message}")
                            if issue.suggestion:
                                st.info(f"💡 {issue.suggestion}")
                            st.divider()
                
                if info_issues:
                    with st.expander(f"ℹ️ **SUGGESTIONS** ({len(info_issues)})", expanded=False):
                        for issue in info_issues:
                            st.markdown(f"**Line {issue.line}:** {issue.message}")
                            if issue.suggestion:
                                st.info(f"💡 {issue.suggestion}")
                            st.divider()
        
        with st.expander("📄 **Full Text Report**", expanded=False):
            report = ReportGenerator.generate_text_report(result)
            st.code(report, language="text")

elif analyze_button and not code_input.strip():
    st.warning("Please enter some code to analyze.")

# Sidebar info based on mode
if st.session_state['mode'] == 'candidate':
    st.sidebar.title("ℹ️ Instructions")
    st.sidebar.markdown("""
**Candidate Mode** - Code Editor

### Supported Languages
- 🐍 Python
- ☕ Java
- 🟨 JavaScript
- #️⃣ C#

### How to Use
1. Select your programming language
2. Write your Selenium automation code
3. Click "Download Code" when finished
4. Submit the downloaded file

### Tips
- Write clean, readable code
- Use proper indentation
- Add comments where needed
- Test your logic before submitting
""")
else:
    st.sidebar.title("ℹ️ About")
    st.sidebar.markdown("""
**Automation Code Verifier** is a tool to analyze Selenium automation code across multiple languages.

### Supported Languages
- 🐍 Python
- ☕ Java
- 🟨 JavaScript
- #️⃣ C#

### What It Checks
- ✅ Syntax validation
- ✅ Missing imports
- ✅ Selenium best practices
- ✅ Wait strategies
- ✅ Resource management
- ✅ Exception handling
- ✅ Locator patterns
- ✅ Anti-patterns

### How to Use
1. Select your programming language
2. Paste your Selenium code
3. Click "Analyze Code"
4. Review issues and suggestions

### Severity Levels
- 🔴 **Critical:** Must fix - prevents code from running
- ⚠️ **Warning:** Should fix - impacts reliability
- ℹ️ **Info:** Consider fixing - improves code quality
""")

st.sidebar.divider()
st.sidebar.markdown("Made with ❤️ by Cliff Ian Murillo")
st.sidebar.markdown("Powered by Streamlit")
