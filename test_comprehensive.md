﻿

Converted Markdown

/* Professional Document Export Styles - Inspired by ConvertAI */
/* Based on best practices from https://github.com/joemccann/ConvertAI */

/* Reset & Base Typography */
* {
 box-sizing: border-box;
}

html {
 font-size: 14px;
 background: #fff;
 color: #373D49;
 -webkit-text-size-adjust: 100%;
}

body {
 font-family: Georgia, Cambria, "Times New Roman", serif;
 font-size: 1rem;
 font-weight: 400;
 line-height: 2rem; /* ConvertAI uses 2rem for better readability */
 margin: 0;
 padding: 2rem;
 max-width: 1024px;
 margin: 0 auto;
}

/* Paragraphs with proper spacing (ConvertAI-style) */
p {
 margin: 0 0 1.33999rem 0;
 padding-top: 0.66001rem;
 font-feature-settings: "kern" 1, "onum" 1, "liga" 1; /* Typography features */
}

/* Lists with proper spacing */
ul, ol {
 margin-bottom: 0.83999rem;
 padding-top: 0.16001rem;
}

li {
 font-feature-settings: "kern" 1, "onum" 1, "liga" 1;
 margin-left: 1rem;
}

li > ul, li > ol {
 margin-bottom: 0;
}

/* Headings with ConvertAI typography */
h1, h2, h3, h4, h5, h6 {
 font-family: "Source Sans Pro", "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
 font-feature-settings: "dlig" 1, "liga" 1, "lnum" 1, "kern" 1;
 font-weight: 600;
 margin-top: 0;
 line-height: 1.3;
 color: #2c3e50;
}

h1 {
 font-size: 2.0571428571rem;
 line-height: 3rem;
 margin-bottom: 0.21999rem;
 padding-top: 0.78001rem;
 border-bottom: 2px solid #e8e8e8;
 padding-bottom: 0.3em;
}

h2 {
 font-size: 1.953125rem;
 line-height: 3rem;
 margin-bottom: 0.18358375rem;
 padding-top: 0.81641625rem;
 border-bottom: 1px solid #e8e8e8;
 padding-bottom: 0.3em;
}

h3 {
 font-size: 1.6457142857rem;
 line-height: 3rem;
 margin-bottom: 0.07599rem;
 padding-top: 0.92401rem;
}

h4 {
 font-size: 1.5625rem;
 margin-bottom: 0.546865rem;
 padding-top: 0.453135rem;
}

h5 {
 font-size: 1.25rem;
 margin-bottom: -0.56251rem;
 padding-top: 0.56251rem;
}

h6 {
 font-size: 1rem;
 margin-bottom: -0.65001rem;
 padding-top: 0.65001rem;
}

h5 {
 font-size: 1.125rem;
}

h6 {
 font-size: 1rem;
 color: #6c757d;
}

/* Paragraphs & Text */
p {
 margin: 0 0 1.25rem;
}

strong, b {
 font-weight: 600;
}

em, i {
 font-style: italic;
}

/* Links with ConvertAI styling */
a {
 color: #35D7BB; /* ConvertAI's teal accent */
 text-decoration: none;
 cursor: pointer;
}

a:hover, a:focus {
 border-bottom-color: #35D7BB;
 color: #2ac5a9;
}

/* Code Blocks - ConvertAI Style */
code {
 color: #c7254e;
 background-color: #f9f2f4;
 padding: 2px 4px;
 border-radius: 4px;
 font-family: "Courier New", Courier, monospace;
 font-size: 0.9em;
}

pre {
 display: block;
 margin: 0 0 1.33999rem;
 padding: 0.66001rem 9.5px 9.5px;
 font-size: 1rem;
 line-height: 2rem;
 word-break: break-all;
 word-wrap: break-word;
 color: #333;
 background: linear-gradient(
 to bottom,
 #fff 0, #fff 0.75rem,
 #f5f7fa 0.75rem, #f5f7fa 2.75rem,
 #fff 2.75rem, #fff 4rem
 );
 background-size: 100% 4rem;
 border: 1px solid #d3daea;
 border-radius: 4px;
 overflow: auto;
}

pre code {
 padding: 0;
 font-size: inherit;
 color: inherit;
 white-space: pre-wrap;
 background-color: transparent;
 border-radius: 0;
}

/* Blockquote - ConvertAI Style */
blockquote {
 margin: 0;
 border-left: 3px solid #A0AABF;
 padding: 0.66001rem 1rem 1rem;
 font-style: italic;
 color: #666;
 background-color: #f9f9f9;
}

blockquote p {
 margin-bottom: 0.33999rem;
 padding-top: 0.66001rem;
 font-size: 1rem;
}

/* Tables - ConvertAI/Bootstrap Style */
table {
 background-color: transparent;
 border-collapse: collapse;
 border-spacing: 0;
}

th {
 text-align: left;
}

.table, table {
 width: 100%;
 max-width: 100%;
 margin-bottom: 20px;
}

.table > thead > tr > th,
table > thead > tr > th {
 padding: 8px;
 line-height: 1.428571429;
 vertical-align: bottom;
 border-top: 1px solid #ddd;
 border-bottom: 2px solid #ddd;
}

.table > thead > tr > td,
.table > tbody > tr > th,
.table > tbody > tr > td,
.table > tfoot > tr > th,
.table > tfoot > tr > td,
table > thead > tr > td,
table > tbody > tr > th,
table > tbody > tr > td,
table > tfoot > tr > th,
table > tfoot > tr > td {
 padding: 8px;
 line-height: 1.428571429;
 vertical-align: top;
 border-top: 1px solid #ddd;
}

/* Bootstrap table-bordered */
.table-bordered,
.table-bordered > thead > tr > th,
.table-bordered > thead > tr > td,
.table-bordered > tbody > tr > th,
.table-bordered > tbody > tr > td,
.table-bordered > tfoot > tr > th,
.table-bordered > tfoot > tr > td {
 border: 1px solid #ddd;
}

.table-bordered > thead > tr > th,
.table-bordered > thead > tr > td {
 border-bottom-width: 2px;
}

/* Bootstrap table-striped */
.table-striped > tbody > tr:nth-child(odd) > td,
.table-striped > tbody > tr:nth-child(odd) > th {
 background-color: #f9f9f9;
}

/* Table hover effect */
.table-hover > tbody > tr:hover > td,
.table-hover > tbody > tr:hover > th {
 background-color: #f5f5f5;
}

/* Horizontal Rule */
hr {
 border: none;
 border-top: 2px solid #e0e0e0;
 margin: 32px 0;
}

/* Images */
img {
 max-width: 100%;
 height: auto;
 margin: 20px 0;
 border-radius: 4px;
 box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

blockquote p {
 margin-bottom: 0.5rem;
}

blockquote p:last-child {
 margin-bottom: 0;
}

/* Tables - Professional Styling */
table {
 width: 100%;
 max-width: 100%;
 margin-bottom: 1.25rem;
 background-color: transparent;
 border-collapse: collapse;
 border-spacing: 0;
}

table th,
table td {
 padding: 0.75rem;
 vertical-align: top;
 border: 1px solid #d0d7de;
 text-align: left;
 line-height: 1.5;
}

table thead th {
 vertical-align: bottom;
 border-bottom: 2px solid #d0d7de;
 background-color: #f6f8fa;
 font-weight: 600;
 color: #24292f;
}

table tbody tr:nth-child(odd) {
 background-color: #f6f8fa;
}

table tbody tr:hover {
 background-color: #f0f3f5;
}

/* Striped Tables */
.table-striped tbody tr:nth-child(odd) {
 background-color: #f9f9f9;
}

/* Bordered Tables */
.table-bordered,
.table-bordered th,
.table-bordered td {
 border: 1px solid #d0d7de;
}

.table-bordered thead th,
.table-bordered thead td {
 border-bottom-width: 2px;
}

/* Horizontal Rules */
hr {
 height: 0.25rem;
 padding: 0;
 margin: 1.5rem 0;
 background-color: #e8e8e8;
 border: 0;
}

/* Images */
img {
 max-width: 100%;
 height: auto;
 border-radius: 4px;
 margin: 1rem 0;
}

/* Task Lists */
input[type="checkbox"] {
 margin-right: 0.5rem;
}

/* Keyboard Keys */
kbd {
 display: inline-block;
 padding: 0.1875rem 0.375rem;
 font-size: 0.875em;
 font-family: "Consolas", "Monaco", "Courier New", monospace;
 color: #24292f;
 background-color: #f6f8fa;
 border: 1px solid #d0d7de;
 border-radius: 3px;
 box-shadow: inset 0 -1px 0 rgba(175, 184, 193, 0.2);
}

/* Responsive Tables */
@media screen and (max-width: 768px) {
 table {
 display: block;
 overflow-x: auto;
 -webkit-overflow-scrolling: touch;
 }

 body {
 padding: 1rem;
 }

 h1 {
 font-size: 1.75rem;
 }

 h2 {
 font-size: 1.5rem;
 }

 h3 {
 font-size: 1.25rem;
 }
}

/* Print Styles */
@media print {
 body {
 font-size: 12pt;
 color: #000;
 }

 h1, h2, h3, h4, h5, h6 {
 page-break-after: avoid;
 }

 pre, blockquote, table, img {
 page-break-inside: avoid;
 }

 a {
 color: #000;
 text-decoration: underline;
 }

 thead {
 display: table-header-group;
 }
}

/* Utility Classes */
.text-center {
 text-align: center;
}

.text-right {
 text-align: right;
}

.text-left {
 text-align: left;
}

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }

﻿\

Comprehensive HTML Test Document

body {\

 font-family: Georgia, ‘Times New Roman’, serif;\

 line-height: 1.8;\

 max-width: 900px;\

 margin: 0 auto;\

 padding: 20px;\

 color: #333;\

 }\

 h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }\

 h2 { color: #34495e; border-bottom: 2px solid #95a5a6; padding-bottom: 8px; }\

 h3 { color: #7f8c8d; }\

 table { border-collapse: collapse; width: 100%; margin: 20px 0; }\

 th, td { border: 1px solid #bdc3c7; padding: 12px; text-align: left; }\

 th { background-color: #3498db; color: white; font-weight: 600; }\

 tr:nth-child(even) { background-color: #ecf0f1; }\

 code { background-color: #f8f9fa; padding: 2px 6px; border-radius: 3px; font-family: ‘Courier New’, monospace; }\

 pre { background-color: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }\

 blockquote { border-left: 4px solid #3498db; margin: 20px 0; padding: 10px 20px; background-color: #ecf0f1; font-style: italic; }\

 .highlight { background-color: #f39c12; padding: 2px 4px; }\

 .footer { margin-top: 40px; padding-top: 20px; border-top: 2px solid #95a5a6; text-align: center; color: #7f8c8d; }

# Comprehensive HTML Test Document

*******Purpose:******* Test all HTML elements for conversion quality

****Created:**** November 10, 2025 | ****Version:**** 1.0

---

## Table of Contents

- [Headings](#headings)
- [Text Formatting](#text)
- [Lists](#lists)
- [Tables](#tables)
- [Code Blocks](#code)
- [Media Elements](#media)
- [Forms](#forms)

---

## 1. Heading Hierarchy

# Heading Level 1

## Heading Level 2

### Heading Level 3

#### Heading Level 4

##### Heading Level 5

###### Heading Level 6

---

## 2. Text Formatting

This is a *******bold text******* and this is *******also bold*******.

This is ****italic text**** and this is ****also italic****.

This is *************bold and italic********* combined.

This is ~~deleted text~~ and this is ~~strikethrough~~.

This is inserted text and this is underlined.

This is highlighted text using the mark element.

This is small text and this is superscript and subscript.

This is `inline code` within a sentence.

This is HTML abbreviation with tooltip.

This is a short inline quotation element.

>

>
> This is a block quotation that can span multiple lines. It’s typically used for longer quotes and provides proper semantic meaning.
>
>
> — Famous Author
>
>
>

Mathematical formula: E = mc2

Chemical formula: H2O

---

## 3. Lists

### 3.1 Unordered List

- First item
- Second item
- Third item with nested list:
	- Nested item 1
	- Nested item 2
	- Deep nested:
		- Level 3 item
- Fourth item

### 3.2 Ordered List

1. First step
2. Second step
3. Third step with nested:
	1. Sub-step A
	2. Sub-step B
	3. Sub-step C
4. Fourth step

### 3.3 Description List

HTML\

HyperText Markup Language - the standard markup language for web pages\

CSS\

Cascading Style Sheets - used for styling HTML documents\

JavaScript\

A programming language that enables interactive web pages

---

## 4. Tables

### 4.1 Simple Table

| Name | Age | City | Occupation |
| --- | --- | --- | --- |
| Alice Johnson | 28 | New York | Software Engineer |
| Bob Smith | 34 | London | Data Scientist |
| Charlie Brown | 45 | Tokyo | Product Manager |

### 4.2 Complex Table with Colspan and Rowspan

| Quarterly Sales Report | Region | Quarter 1 | Total |
| --- | --- | --- | --- |
| Jan | Feb | Mar |
| North | $10,000 | $12,000 | $15,000 | $37,000 |
| South | $8,000 | $9,500 | $11,000 | $28,500 |
| East | $12,000 | $14,000 | $13,500 | $39,500 |
| Total | $30,000 | $35,500 | $39,500 | $105,000 |
| — | — | — | — | — |

---

## 5. Code Blocks

### 5.1 Inline Code

Use the `print()` function to display output in Python.

In JavaScript, use `console.log()` for debugging.

### 5.2 Preformatted Code Block

```
def calculate_fibonacci(n):
    """
    Calculate the nth Fibonacci number
    Args:
        n (int): Position in sequence
    Returns:
        int: Fibonacci number
    """
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Test
for i in range(10):
    print(f"F({i}) = {calculate_fibonacci(i)}")

```

### 5.3 SQL Query Example

```
SELECT
    customers.name,
    COUNT(orders.id) as total_orders,
    SUM(orders.amount) as total_spent
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
WHERE orders.order_date >= '2024-01-01'
GROUP BY customers.name
HAVING total_orders > 5
ORDER BY total_spent DESC
LIMIT 10;

```

---

## 6. Media Elements

### 6.1 Images

![Placeholder image](https://via.placeholder.com/400x200)\

Figure 1: This is a sample image with caption

### 6.2 Links

Visit [Google](https://www.google.com) for search.

Internal link: [Jump to Headings section](#headings)

Email link: [example@email.com](mailto:example@email.com)

### 6.3 Embedded Content

Video and audio elements would go here (not included to keep file size small).

---

## 7. Form Elements

User Information

Name:

Email:

Age:

Country:

Select a country\

United States\

United Kingdom\

Canada\

Australia

Gender:\

 Male\

 Female\

 Other

Interests:\

 Coding\

 Reading\

 Sports

Message:

Submit\

Reset

---

## 8. Semantic HTML5 Elements

### Article Title

November 10, 2025

This is the article content. Articles are self-contained compositions that could be independently distributed.

Article footer with additional information

#### Sidebar Information

This is sidebar content that provides supplementary information.

Click to expand details\

This content is hidden by default and can be toggled by clicking the summary.

---

## 9. Special Characters & Entities

< Less than

>
> Greater than
>
>
>

& Ampersand

" Quote

' Apostrophe

© Copyright

® Registered

™ Trademark

€ Euro

£ Pound

¥ Yen

---

*******Document Summary*******

This comprehensive HTML document includes:

- ✓ All heading levels (h1-h6)
- ✓ Text formatting (bold, italic, underline, strike, etc.)
- ✓ Lists (unordered, ordered, description)
- ✓ Tables (simple and complex with colspan/rowspan)
- ✓ Code blocks (inline and preformatted)
- ✓ Forms (inputs, select, radio, checkbox, textarea)
- ✓ Semantic HTML5 elements (article, aside, details)
- ✓ Special characters and entities

****Total: 9 sections covering 60+ HTML elements****

---

© 2025 ConverterAI | Comprehensive Test Suite v1.0
