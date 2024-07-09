INSTRUCTIONS:
- This is a template. Please replace the content while keeping this structure.
- Make sure to read our contribution guide to learn how to submit your content to Tilburg Science Hub.
- Always start your file with the parameters shown below. Keep the double quotes as shown.
- Do NOT use #Titles with a single # in your article. Instead, use the title parameter shown below.
- Please provide up to 10 keywords for this Building Block in the appropriate parameter. Metadata should provide information on the role and usage of this Building Block (e.g., "data collection, data analysis, article writing")
- IMPORTANT! Replace the # of the weight parameter with an integer (no quotes are needed). This number indicates the position of this article within its section (folder). The ordering of all articles inside a folder is based on their weight. Articles with lower weight appear at the top.
- If you want to be credited, fill in the author and authorlink fields below. If you want to remain anonymous, delete those.
- Provide at least one short link for your article. Combine an action verb and a noun like this: /verb/noun (ex. /install/python).
- Remove these instructions before submitting. Your article should start with the three dashes --- and the following parameters.
---
title: "Your building block title (50-70 characters + most important keyword must be in the title atleast once)"
description: "A brief description of this tutorial page (130–160 characters + most important keyword must be in the descripion atleast once)."
keywords: "any, relevant, keywords, separated, by, commas, like, this"
date: YYYY-MM-DD
weight: #
author: "Your Name"
authorlink: "A link to your personal webpage"
aliases:
  - /verb/noun
  - /do/this
  - /get/that
  - add as many as you want, but at least one
---

## Overview <!-- Goal of the Building Block -->

Provide a brief overview of the issue to solve, or describe why this is a best practice.

Add any special requirements or attach a dummy data set if needed.


## Code <!-- Provide your code in all the relevant languages and/or operating systems and specify them after the three back ticks. Do NOT remove % codeblock % -->

{{% codeblock %}} <!-- You can provide more than one language in the same code block -->

[python-link](code.py) <!-- OPTIONAL: You can also provide your code as a downloadable file (useful for very long codes). Make sure you place this file in the same folder. Specify in [square brackets] the language followed by "-link" as shown here.-->


```python
# some Python code here
print("Hello, world!")
```

```R
# some R code here
cat('Hello, world!')
```

{{% /codeblock %}}


## Examples

Provide examples to support the solution.

{{% example %}}

This is an example. It will be formatted differently to grab the viewer's attention.

{{% /example %}}


### You can use third- or fourth-level headers like this one

Provide examples in different programming languages and/or operating systems.

{{% tip %}}

**This is a tip.**

You can use special formatting options to highlight some paragraphs in your article.

{{% /tip %}}

{{% warning %}}

And this is a warning.

{{% /warning %}}

## Advanced use cases or "See also"

Illustrate advanced use cases and explain how to bring this to the next level.

Provide useful resources and link to "see also" articles.

{{% summary %}}

Lastly, include a brief summary to wrap up your article.

{{% /summary %}}
