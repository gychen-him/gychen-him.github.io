---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
layout: spa
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

I am a Research Professor at Hangzhou Institute of Medicine, Chinese Academy of Sciences, and Associate Director of the Medical AI Center. Previously, I served as a Hundred Talents Program Research Professor at the Zhejiang University-Zhijiang Laboratory Platform. I received my Ph.D. in Computer Science and Engineering from The Chinese University of Hong Kong.

My research focuses on developing next-generation computational tools for medical AI and drug discovery, with particular emphasis on leveraging modern artificial intelligence methods, especially large language models, to accelerate pharmaceutical research and development. My research follows a comprehensive pipeline: processing clinical multimodal information to uncover disease mechanisms, and subsequently designing targeted therapeutics to modulate biological functions. I lead a team developing intelligent platforms for drug discovery and have achieved breakthroughs in core algorithms for drug virtual screening workflows, including protein representation, pocket detection, conformational docking, molecular generation, and activity scoring.

I have published over 40 papers as first or corresponding author in prestigious journals and conferences including *Nature Machine Intelligence*, *Nature Computational Science*, *Nature Communications*, ICML, ICLR, and NeurIPS. I currently lead several major research projects including National Key R&D Program International Cooperation Projects and National Natural Science Foundation projects.

## Join Our Team
We are always looking for talented and motivated researchers to join our team. If you are interested in, please feel free to contact me with your CV and research interests.

Email: chenguangyong@him.cas.cn

# News
- *2025.01*: **[Nature Communications]** Our work **PhyloTune** (Corresponding Author) is accepted! We developed an efficient method to accelerate phylogenetic updates using a pretrained DNA language model, achieving significant speedup in evolutionary analysis.
- *2025.01*: **[Nature Communications]** Our work on **Unified Molecular Representation** (Corresponding Author) is accepted! We developed an explainable molecular representation learning method for imperfectly annotated data from a hypergraph perspective.
- *2025.01*: **[JACS]** Our research on **Small CAG Repeat RNA** (Corresponding Author) is published! We discovered that these RNAs form duplex structures with sticky ends that promote RNA condensation, providing new insights into repeat-expansion diseases.
- *2025.01*: **[Advanced Science]** Our paper **scHeteroNet** (Corresponding Author) is accepted! We proposed a heterophily-aware graph neural network for accurate cell type annotation and novel cell detection in single-cell analysis.
- *2025.01*: **[Bioinformatics]** Our paper **DivPro** (Corresponding Author) is accepted! It introduces a novel approach for diverse protein sequence design with direct structure recovery guidance, enhancing the efficiency of protein engineering.
- *2025.01*: **[ICCV 2025]** Our work **ChemMiner** is accepted! We developed a Large Language Model Agent system for automated chemical literature data mining.