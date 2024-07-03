---
title: "Test new website"
description: "Valerie testing the new cool website"
keywords: "test, website, flask"
draft: false
weight: 1
date: 2021-01-06T22:01:14+05:30
author: "Valerie Vossen,Krzysztof Wiesniakowski"
aliases:
  - /shiftshare
---

# Overview

## Codeblock

{{% codeblock %}}
```R
# Install and load the ShiftShareSE package
install.packages("ShiftShareSE")
library(ShiftShareSE)
```
{{% /codeblock %}}

## List

The code contains the following terms:

  - list item 1 
  - list item 2

1. point one 
2. point two
    - point two.2
    

## Tables

{{% table %}}
| Context                                        | Shift-Share Instrument                                | Authors                                    |
|-------------------------------------------|----------------------------------------------------|--------------------------------------------------|
| Employment impact <br> on wage growth <br> in region `l` | *Predicted employment due to <br> national industry trends* <br><br> **Shifts:** National growth of industry `n` <br> **Shares:** Lagged employment <br> shares of industry in region `l` | [Bartik (1991)](https://research.upjohn.org/up_press/77/); <br> [Blanchard & <br> Katz (1992)](https://www.aeaweb.org/articles?id=10.1257/aer.89.2.69)  |
| Local labor market effects <br> of rising Chinese import <br> competition in the US | *Predicted growth of <br> import competition* <br><br> **Shifts:** Growth of China exports <br> in manufacturing industry `n` <br> **Shares:** 10-year lagged <br> employment shares over total <br> employment in region `l` | [Autor, Dorn, <br> and Hanson <br> (2013)](https://www.aeaweb.org/articles?id=10.1257/aer.103.6.2121)  |
| Import impact by <br> Danish firm on wages  | *Predicted change in firm inputs <br> via transport costs*<br><br> **Shifts:** Changes in transport <br> costs by `n` = (product, country) <br> **Shares:** Lagged import shares  | [Hummels <br> et al. (2014)](https://www.aeaweb.org/articles?id=10.1257/aer.104.6.1597)  |
{{% /table %}}


## Math equations

$UR_{i,t} = \beta_0 + \beta_1 IM_{i,t} + \beta_2 X_{i,t} + \epsilon_{i,t}$

## image test

<p align = "center">
<img src = "../images/corr_cause.png" width="400">
<figcaption> Regression output </figcaption>
</p>



{{% tip %}}
The shift-share instrument is a powerful tool for addressing endogeneity issues in regional economic studies. By decomposing the endogenous shift into a weighted average of shifts and shares that vary on other levels, an exogenous instrument can be used.
{{% /tip %}}


{{% summary %}}
The shift-share instrument is a powerful tool for addressing endogeneity issues in regional economic studies. By decomposing the endogenous shift into a weighted average of shifts and shares that vary on other levels, an exogenous instrument can be used.
{{% /summary %}}

