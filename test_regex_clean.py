"""Quick test of regex patterns"""
import re

# Read test file
with open('test_comprehensive.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"Original length: {len(html_content)}")
print(f"Contains <style>: {'<style>' in html_content}")
print(f"Contains </style>: {'</style>' in html_content}")
print()

# Test regex
html_cleaned = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
html_cleaned = re.sub(r'<script[^>]*>.*?</script>', '', html_cleaned, flags=re.DOTALL | re.IGNORECASE)

print(f"Cleaned length: {len(html_cleaned)}")
print(f"Contains <style> after cleaning: {'<style>' in html_cleaned}")
print(f"Contains font-family: after cleaning: {'font-family:' in html_cleaned}")
print()

# Show first 500 chars
print("First 500 chars after cleaning:")
print("="*60)
print(html_cleaned[:500])
print("="*60)
