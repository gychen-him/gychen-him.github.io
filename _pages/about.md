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

# Research Group
<div class="group-members" style="gap: 1.5em; justify-content: center;">
  <!-- Show a few key members or just a compact grid -->
  <div class="member-item" style="width: 150px; min-width: 150px; margin-bottom: 1.5em;">
    <div class="member-photo-container" style="width: 120px; height: 150px;">
      <div class="member-photo-inner">
        <img src="/images/members/formal/博后-孟昭政.jpg" class="photo-front" alt="孟昭政 (Zhaozheng Meng)">
        <img src="/images/members/life/博后-孟昭政.jpg" class="photo-back" alt="孟昭政 (Zhaozheng Meng)">
      </div>
    </div>
    <div class="member-info">
      <h4 style="font-size: 0.95em;">孟昭政 (Z. Meng)</h4>
    </div>
  </div>
  <div class="member-item" style="width: 150px; min-width: 150px; margin-bottom: 1.5em;">
    <div class="member-photo-container" style="width: 120px; height: 150px;">
      <div class="member-photo-inner">
        <img src="/images/members/formal/博后-王帅.jpg" class="photo-front" alt="王帅 (Shuai Wang)">
        <img src="/images/members/life/博后-王帅.jpg" class="photo-back" alt="王帅 (Shuai Wang)">
      </div>
    </div>
    <div class="member-info">
      <h4 style="font-size: 0.95em;">王帅 (S. Wang)</h4>
    </div>
  </div>
  <div class="member-item" style="width: 150px; min-width: 150px; margin-bottom: 1.5em;">
    <div class="member-photo-container" style="width: 120px; height: 150px;">
      <div class="member-photo-inner">
        <img src="/images/members/formal/博后-郭颖.jpg" class="photo-front" alt="郭颖 (Ying Guo)">
        <img src="/images/members/life/博后-郭颖.jpg" class="photo-back" alt="郭颖 (Ying Guo)">
      </div>
    </div>
    <div class="member-info">
      <h4 style="font-size: 0.95em;">郭颖 (Y. Guo)</h4>
    </div>
  </div>
  <div class="member-item" style="width: 150px; min-width: 150px; margin-bottom: 1.5em;">
    <div class="member-photo-container" style="width: 120px; height: 150px;">
      <div class="member-photo-inner">
        <img src="/images/members/formal/博后-齐晨.jpg" class="photo-front" alt="齐晨 (Chen Qi)">
        <img src="/images/members/life/博后-齐晨.jpg" class="photo-back" alt="齐晨 (Chen Qi)">
      </div>
    </div>
    <div class="member-info">
      <h4 style="font-size: 0.95em;">齐晨 (C. Qi)</h4>
    </div>
  </div>
  <div class="member-item" style="width: 150px; min-width: 150px; margin-bottom: 1.5em;">
    <div class="member-photo-container" style="width: 120px; height: 150px;">
      <div class="member-photo-inner">
        <img src="/images/members/formal/2025博-天大-刘心欣.jpg" class="photo-front" alt="刘心欣 (Xinxin Liu)">
        <img src="/images/members/life/2025博-天大-刘心欣.jpg" class="photo-back" alt="刘心欣 (Xinxin Liu)">
      </div>
    </div>
    <div class="member-info">
      <h4 style="font-size: 0.95em;">刘心欣 (X. Liu)</h4>
    </div>
  </div>
</div>
<p style="text-align: right; margin-top: -1em;"><a href="/group/">View all members →</a></p>

# News
- *2025.01*: **[Nature Communications]** Our work **PhyloTune** is accepted! We developed an efficient method to accelerate phylogenetic updates using a pretrained DNA language model, achieving significant speedup in evolutionary analysis.
- *2025.01*: **[Bioinformatics]** Our paper **DivPro** is accepted! It introduces a novel approach for diverse protein sequence design with direct structure recovery guidance, enhancing the efficiency of protein engineering.
- *2025.01*: **[JACS]** Our research on **Small CAG Repeat RNA** is published! We discovered that these RNAs form duplex structures with sticky ends that promote RNA condensation, providing new insights into repeat-expansion diseases.
- *2025.01*: **[Nature Communications]** Our work on **Unified Molecular Representation** is accepted! We developed an explainable molecular representation learning method for imperfectly annotated data from a hypergraph perspective.
- *2025.01*: **[ICCV 2025]** Our work **ChemMiner** is accepted! We developed a Large Language Model Agent system for automated chemical literature data mining.