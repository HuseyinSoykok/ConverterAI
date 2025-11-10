## Page 1

Milestone 1 Report: Titanic Dataset Analysis (Data-Verified) A. Title & Source Dataset Title: Titanic - Machine Learning from Disaster Primary URL: https://www.kaggle.com/datasets/shuofxz/titanic-machine-learning- from-disaster Publisher/Author: shuofxz (via Kaggle Datasets) License / Usage Terms: CC0: Public Domain B. Motivation This dataset is of interest as it provides a compelling, real-world case study for data analysis, allowing for the exploration of socio-economic factors influencing survival during a major historical event. Visualizing this data can reveal tangible patterns of human behavior and societal structure under duress.

**My two concrete questions for visualization are:**

1. How do survival rates (Survived) compare across different passenger classes (Pclass) and genders (Sex)? 2. What is the correlation between passenger age (Age) and the ticket fare (Fare), and how do these two variables jointly impact survival outcomes? C. Scope & Granularity The dataset consists of two files: train.csv  and test.csv . This analysis focuses primarily on train.csv , as it contains the Survived  attribute essential for visualization. Size: The train.csv  file contains 891 records (rows) and 12 attributes (columns). Unit of Analysis: One row represents a single passenger. Keys: The PassengerId  attribute serves as a unique identifier (key) for each passenger. D. Schema (Types & Ranges) The items (entities) are the 891 passengers. The following table details their attributes based on the train.csv  file, classifying each as quantitative, categorical, or ordinal. Attribute Role Type Range / Domain & Unit PassengerId ID/Key Quantitative [1, 891] Survived Attribute Categorical Binary Domain: 0 (No), 1 (Yes) Pclass Attribute Ordinal Ordered Domain: 1 (1st) > 2 (2nd) > 3 (rd) Name Attribute Categorical High-Cardinality Domain (891 unique values) Sex Attribute Categorical Binary Domain: male, female



---

## Page 2

Age Attribute Quantitative Min: 0.42, Max: 80.0 (Unit: Years) SibSp Attribute Quantitative Discrete Domain: [0, 8] (Unit: Count of Persons) Parch Attribute Quantitative Discrete Domain: [0, 6] (Unit: Count of Persons) Ticket Attribute Categorical High-Cardinality Domain (681 unique values) Fare Attribute Quantitative Min: 0.0, Max: 512.33 (Unit: Currency) Cabin Attribute Categorical High-Cardinality Domain (147 unique values) Embarked Attribute Categorical Domain: C (Cherbourg), Q (Queenstown), S (Southampton) F. Quality & Limitations Analysis of train.csv  reveals several data quality issues that will affect visualization.

**Missing Values:**

Age : 177 values (19.87%) are missing. This is a significant gap requiring an imputation strategy (e.g., using the median) or explicit visualization as an "Unknown Age" category. Cabin : 687 values (77.10%) are missing. The vast majority of cabin data is unknown, making this attribute unreliable for comprehensive analysis. Embarked : 2 values (0.22%) are missing. This is a minor issue, likely solvable by imputing the most frequent port ('S').

**Data Inconsistencies & Outliers:**

Fare : This attribute has a minimum value of 0.0 and a maximum of 512.33, with a 75th percentile of only 31.0. This extreme skew and the presence of zero-fares are outliers that must be handled (e.g., using a log scale for visualization). Ticket  & Cabin : These categorical attributes have very high cardinality (681 and 147 unique values, respectively) and inconsistent formats, making them unsuitable for direct categorical visualization.

**Sampling Bias:**

The train.csv  file (891 records) is a sample of the full passenger manifest (approx. 2,224). This represents a selection bias, and any conclusions drawn from visualizations are only representative of this sample, not the entire population of the disaster. G. Suitability This dataset is "about right" for the project. Size & Complexity: At 891 rows, the dataset is large enough to show meaningful patterns but small enough to be easily managed, fitting the "1,000-100,000 rows" guideline's lower end. It is tabular and requires no complex joins.



---

## Page 3

"Not too easy": The dataset requires mandatory cleaning (handling 19.87% missing Age  data) and thoughtful feature engineering (e.g., binning Age  or creating FamilySize  from SibSp  and Parch ), preventing it from being a "toy table". Richness of Attributes: It provides a perfect mix of quantitative ( Age , Fare ), categorical ( Sex , Embarked ), and ordinal ( Pclass ) attributes, which supports multiple meaningful visual perspectives and allows for experimentation with different encodings as suggested by the guidelines. PII Compliance: The dataset does not contain personally identifiable information (PII) in a sensitive context; names are historical and publicly known, satisfying the project's ethical requirements.

