# Comprehensive Markdown Test Document

This document contains **all standard Markdown elements** to test conversion quality.

---

## 1. Headings Hierarchy

# Heading Level 1
## Heading Level 2
### Heading Level 3
#### Heading Level 4
##### Heading Level 5
###### Heading Level 6

---

## 2. Text Formatting

This is a **bold text** and this is __also bold__.

This is *italic text* and this is _also italic_.

This is ***bold and italic*** combined.

This is ~~strikethrough~~ text.

This is `inline code` within a sentence.

---

## 3. Paragraphs and Line Breaks

This is the first paragraph. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

This is the second paragraph. Ut enim ad minim veniam, quis nostrud exercitation ullamco 
laboris nisi ut aliquip ex ea commodo consequat.

This is a paragraph with a  
hard line break using two spaces.

---

## 4. Lists

### Unordered List

- First item
- Second item
- Third item
  - Nested item 1
  - Nested item 2
    - Deeply nested item
- Fourth item

### Ordered List

1. First step
2. Second step
3. Third step
   1. Sub-step A
   2. Sub-step B
4. Fourth step

### Task List

- [x] Completed task
- [x] Another completed task
- [ ] Pending task
- [ ] Another pending task

---

## 5. Links and Images

[This is a link to Google](https://www.google.com)

[This is a link with title](https://www.github.com "GitHub Homepage")

Direct URL: https://www.example.com

Email: example@email.com

Image syntax (placeholder):
![Alt text for image](https://via.placeholder.com/400x200)

---

## 6. Code Blocks

### Inline Code

Use the `print()` function to display output.

### Fenced Code Block (Python)

```python
def fibonacci(n):
    """Calculate Fibonacci sequence"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

### Fenced Code Block (JavaScript)

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}

// Arrow function
const square = (x) => x * x;

greet("World");
console.log(square(5));
```

### Fenced Code Block (SQL)

```sql
SELECT 
    customers.name,
    orders.order_date,
    SUM(order_items.quantity * order_items.price) AS total
FROM customers
JOIN orders ON customers.id = orders.customer_id
JOIN order_items ON orders.id = order_items.order_id
WHERE orders.order_date >= '2024-01-01'
GROUP BY customers.name, orders.order_date
ORDER BY total DESC;
```

---

## 7. Tables

### Simple Table

| Name | Age | City |
|------|-----|------|
| Alice | 28 | New York |
| Bob | 34 | London |
| Charlie | 45 | Tokyo |

### Complex Table with Alignment

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Row 1 Col 1  | Row 1 Col 2    | Row 1 Col 3   |
| Row 2 Col 1  | Row 2 Col 2    | Row 2 Col 3   |
| Row 3 Col 1  | Row 3 Col 2    | Row 3 Col 3   |

### Table with Different Content Types

| Feature | Status | Priority | Notes |
|---------|--------|----------|-------|
| User Authentication | ✅ Complete | High | OAuth 2.0 implemented |
| Database Optimization | 🔄 In Progress | Medium | Indexing required |
| API Documentation | ❌ Not Started | Low | Swagger integration |
| Performance Testing | ✅ Complete | High | 99.9% uptime |

---

## 8. Blockquotes

> This is a simple blockquote.
> It can span multiple lines.

> **Nested blockquote example:**
> 
> > This is a nested quote.
> > It provides additional context.
> 
> Back to the first level quote.

---

## 9. Horizontal Rules

This is some text before the horizontal rule.

---

This is some text after the horizontal rule.

***

Another horizontal rule above.

___

And one more horizontal rule.

---

## 10. Mixed Content Example

Here's a **real-world scenario** combining multiple elements:

### Project Requirements

The following features are required for the *ConverterAI* project:

1. **File Format Support**
   - PDF conversion with [PyMuPDF](https://pymupdf.readthedocs.io/)
   - DOCX handling using `python-docx`
   - Markdown processing with `markdown2`

2. **Quality Assurance**
   - [ ] Unit tests for all converters
   - [x] Integration tests
   - [ ] Performance benchmarks

3. **Documentation**
   
   > "Good documentation is as important as good code."
   > — Software Engineering Best Practices

### Performance Metrics

| Converter | Speed (ms) | Accuracy | Memory Usage |
|-----------|------------|----------|--------------|
| PDF → MD  | 45ms       | 95%      | 12 MB        |
| MD → HTML | 8ms        | 99%      | 3 MB         |
| DOCX → MD | 120ms      | 92%      | 18 MB        |

### Sample Code Integration

```python
from converters import UniversalConverter

# Initialize converter
converter = UniversalConverter()

# Convert PDF to Markdown
result = converter.convert(
    input_file="document.pdf",
    output_file="output.md"
)

if result.success:
    print(f"✅ Conversion completed in {result.processing_time:.2f}s")
else:
    print(f"❌ Error: {result.error}")
```

---

## 11. Special Characters and Unicode

### Mathematical Symbols

- α (alpha), β (beta), γ (gamma)
- ∑ (summation), ∫ (integral), √ (square root)
- ≈ (approximately), ≠ (not equal), ≤ (less than or equal)

### Currency Symbols

- Dollar: $100
- Euro: €200
- Pound: £300
- Yen: ¥400

### Arrows and Symbols

← ↑ → ↓ ↔ ↕ ⇐ ⇑ ⇒ ⇓

✓ ✗ ★ ☆ ♠ ♣ ♥ ♦

---

## 12. Footnotes

Here's a sentence with a footnote[^1].

Here's another sentence with a footnote[^2].

[^1]: This is the first footnote. It provides additional information.

[^2]: This is the second footnote. It can contain **formatting** and [links](https://example.com).

---

## 13. Definition Lists (Extended Markdown)

Term 1
: Definition for term 1

Term 2
: Definition for term 2a
: Definition for term 2b

---

## 14. Subscript and Superscript

Water molecule: H~2~O

Einstein's equation: E = mc^2^

---

## Conclusion

This comprehensive test document includes:

- ✅ All heading levels (h1-h6)
- ✅ Text formatting (bold, italic, strikethrough)
- ✅ Lists (unordered, ordered, nested, task lists)
- ✅ Links and images
- ✅ Code blocks (inline and fenced)
- ✅ Tables (simple and complex)
- ✅ Blockquotes (single and nested)
- ✅ Horizontal rules
- ✅ Special characters and Unicode
- ✅ Footnotes
- ✅ Mixed content scenarios

**Total Elements:** 14 sections covering 50+ Markdown features

---

*Document created on November 10, 2025*  
*Version 1.0*  
*ConverterAI Comprehensive Test Suite*
